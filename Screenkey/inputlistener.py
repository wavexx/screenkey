# -*- coding: utf-8 -*-
# Distributed under the GNU GPLv3+ license, WITHOUT ANY WARRANTY.
# Copyright(c) 2015: wave++ "Yuri D'Elia" <wavexx@thregr.org>
#
# Outputting translated X11 keystrokes is not a simple problem as soon as XIM
# is introduced: getting an updated keyboard/modifier map is not enough to
# replicate the [complex] logic hidden in the input method.
#
# For this reason we use a fairly convoluted mechanism: we record keystrokes
# using the XRecord extension, but we relay them to another fake window running
# on the same server. By manipulating the event, we trick the input method to
# perform composition for us, and poll for translated output events using
# Xutf8LookupString. Since we cannot determine the state of the input context
# for the target window (we're recording blindly), we also need to reset
# context state carefully when the user switches the active focus. 3(!) extra
# connections to the display server are required for this task, and since we're
# using blocking APIs, having to run on our own thread means we cannot share
# any of those with the regular process. On the other hand, many other keycode
# translation issues are avoided by using the string lookup directly.
#
# This is, of course, never going to be always identical to the final output,
# since we're guessing the state of the client (we do the same when guessing
# the result of backspace anyway). But incidentally this method would also
# allow us to poll the input mechanism while composing, to better reflect the
# actual typing on the keyboard.
#
# Some of the code /could/ have been simplified by using XCB for protocol
# translation, but since there's no equivalent to XKB/XIM, I found the exercise
# futile. Needing to use XIM directly also barred pure-python equivalents. As
# a result, we have to drop back to ctypes for _extra_ phun.
#
# Drop me a line if you ever find this comment helpful, as finding a decent
# solution was not trivial -- YD 21/08/2015.

from __future__ import unicode_literals, absolute_import

if __name__ == '__main__':
    import xlib
    import keysyms
else:
    from . import xlib
    from . import keysyms

import sys
if sys.version_info.major < 3:
    import glib
else:
    import gi
    from gi.repository import GLib as glib

import threading
import warnings
import select


# convenience wrappers
def coalesce_ranges(ranges):
    ranges = sorted(ranges, key=lambda x: x[0])
    ret = ranges[:1]
    for r in ranges[1:]:
        if ret[-1][1] < r[0] - 1:
            ret.append(r)
        else:
            ret[-1][1] = max(ret[-1][1], r[1])
    return ret


def record_context(dpy, ev_ranges, dev_ranges):
    ev_ranges = coalesce_ranges(ev_ranges)
    dev_ranges = coalesce_ranges(dev_ranges)

    specs = max(len(ev_ranges), len(dev_ranges))
    range_specs = (xlib.POINTER(xlib.XRecordRange) * specs)()

    for i in range(specs):
        range_specs[i] = xlib.XRecordAllocRange()
        if len(ev_ranges) > i:
            range_specs[i].contents.delivered_events.first = ev_ranges[i][0]
            range_specs[i].contents.delivered_events.last = ev_ranges[i][1]
        if len(dev_ranges) > i:
            range_specs[i].contents.device_events.first = dev_ranges[i][0]
            range_specs[i].contents.device_events.last = dev_ranges[i][1]

    rec_ctx = xlib.XRecordCreateContext(
        dpy, 0,
        xlib.byref(xlib.c_ulong(xlib.XRecordAllClients)), 1,
        range_specs, specs)

    for i in range(specs):
        xlib.XFree(range_specs[i])

    return rec_ctx


def record_enable(dpy, rec_ctx, callback):
    def intercept(data):
        if data.category != xlib.XRecordFromServer:
            return
        if data.client_swapped:
            warnings.warn("cannot handle swapped protocol data")
            return
        ev = xlib.XWireToEvent(dpy, data.data)
        callback(ev)

    def intercept_(_, data):
        intercept(data.contents)
        xlib.XRecordFreeData(data)

    proc = xlib.XRecordInterceptProc(intercept_)
    xlib.XRecordEnableContextAsync(dpy, rec_ctx, proc, None)
    return proc


def create_replay_window(dpy):
    win_attr = xlib.XSetWindowAttributes()
    win_attr.override_redirect = True
    win = xlib.XCreateWindow(dpy, xlib.XDefaultRootWindow(dpy),
                             0, 0, 1, 1, 0,
                             xlib.CopyFromParent, xlib.InputOnly, None,
                             xlib.CWOverrideRedirect,
                             xlib.byref(win_attr))
    return win


def phantom_release(dpy, kev):
    if not xlib.XPending(dpy):
        return False
    ev = xlib.XEvent()
    xlib.XPeekEvent(dpy, xlib.byref(ev))
    return (ev.type == xlib.KeyPress and \
            ev.xkey.state == kev.state and \
            ev.xkey.keycode == kev.keycode and \
            ev.xkey.time == kev.time)


def keysym_to_unicode(keysym):
    if 0x01000000 <= keysym <= 0x0110FFFF:
        return unichr(keysym - 0x01000000)
    keydata = keysyms.KEYSYMS.get(keysym)
    if keydata is not None:
        return keydata[0]
    return None



class KeyData():
    def __init__(self, pressed=None, filtered=None, repeated=None,
                 string=None, keysym=None, status=None, symbol=None,
                 mods_mask=None, modifiers=None):
        self.pressed = pressed
        self.filtered = filtered
        self.repeated = repeated
        self.string = string
        self.keysym = keysym
        self.status = status
        self.symbol = symbol
        self.mods_mask = mods_mask
        self.modifiers = modifiers


class InputType:
    keyboard = 0b001
    button   = 0b010
    movement = 0b100
    all      = 0b111



class InputListener(threading.Thread):
    def __init__(self, callback, input_types=InputType.all, kbd_compose=True, kbd_translate=True):
        super(InputListener, self).__init__()
        self.callback = callback
        self.input_types = input_types
        self.kbd_compose = kbd_compose
        self.kbd_translate = kbd_translate
        self.lock = threading.Lock()
        self.stopped = True


    def _event_received(self, ev):
        if xlib.KeyPress <= ev.type <= xlib.MotionNotify:
            xlib.XSendEvent(self.replay_dpy, self.replay_win, False, 0, ev)
        elif ev.type in [xlib.FocusIn, xlib.FocusOut]:
            # Forward the event as a custom message in the same queue instead
            # of resetting the XIC directly, in order to preserve queued events
            fwd_ev = xlib.XEvent()
            fwd_ev.type = xlib.ClientMessage
            fwd_ev.xclient.message_type = self.custom_atom
            fwd_ev.xclient.format = 32
            fwd_ev.xclient.data[0] = ev.type
            xlib.XSendEvent(self.replay_dpy, self.replay_win, False, 0, fwd_ev)


    def _event_callback(self, data):
        self.callback(data)
        return False

    def _event_processed(self, data):
        data.symbol = xlib.XKeysymToString(data.keysym)
        if data.string is None:
            data.string = keysym_to_unicode(data.keysym)
        glib.idle_add(self._event_callback, data)


    def _event_modifiers(self, kev, data):
        data.modifiers = modifiers = {}
        modifiers['shift'] = bool(kev.state & xlib.ShiftMask)
        modifiers['caps_lock'] = bool(kev.state & xlib.LockMask)
        modifiers['ctrl'] = bool(kev.state & xlib.ControlMask)
        modifiers['alt'] = bool(kev.state & xlib.Mod1Mask)
        modifiers['num_lock'] = bool(kev.state & xlib.Mod2Mask)
        modifiers['hyper'] = bool(kev.state & xlib.Mod3Mask)
        modifiers['super'] = bool(kev.state & xlib.Mod4Mask)
        modifiers['alt_gr'] = bool(kev.state & xlib.Mod5Mask)


    def _event_keypress(self, kev, data):
        buf = xlib.create_string_buffer(16)
        keysym = xlib.KeySym()
        status = xlib.Status()
        ret = xlib.Xutf8LookupString(self.replay_xic, kev, buf, len(buf),
                                     xlib.byref(keysym), xlib.byref(status))
        if ret != xlib.NoSymbol:
            if 32 <= keysym.value <= 126:
                # avoid ctrl sequences, just take the character value
                data.string = chr(keysym.value)
            else:
                try:
                    data.string = buf.value.decode('utf-8')
                except UnicodeDecodeError:
                    pass
        data.keysym = keysym.value
        data.status = status.value


    def _event_lookup(self, kev, data):
        # this is mostly for debugging: we do not account for group/level
        data.keysym = xlib.XkbKeycodeToKeysym(kev.display, kev.keycode, 0, 0)


    def start(self):
        self.lock.acquire()
        self.stopped = False
        super(InputListener, self).start()


    def stop(self):
        with self.lock:
            if not self.stopped:
                self.stopped = True
                xlib.XRecordDisableContext(self.control_dpy, self.record_ctx)


    def _kbd_init(self):
        if self.kbd_compose:
            style = xlib.XIMPreeditNothing | xlib.XIMStatusNothing
        else:
            style = xlib.XIMPreeditNone | xlib.XIMStatusNone

        # TODO: implement preedit callbacks for on-the-spot composition
        #       (this would fix focus-stealing for the global IM state)
        self.replay_xim = xlib.XOpenIM(self.replay_dpy, None, None, None)
        if not self.replay_xim:
            raise Exception("Cannot initialize input method")

        self.replay_xic = xlib.XCreateIC(self.replay_xim,
                                         xlib.XNClientWindow, self.replay_win,
                                         xlib.XNInputStyle, style,
                                         None)
        xlib.XSetICFocus(self.replay_xic)


    def _kbd_del(self):
        xlib.XDestroyIC(self.replay_xic)
        xlib.XCloseIM(self.replay_xim)


    def _kbd_process(self, ev, last_ev):
        if ev.type == xlib.ClientMessage and \
           ev.xclient.message_type == self.custom_atom:
            if ev.xclient.data[0] in [xlib.FocusIn, xlib.FocusOut]:
                # we do not keep track of multiple XICs, just reset
                xic = xlib.Xutf8ResetIC(self.replay_xic)
                if xic is not None: xlib.XFree(xic)
                return
            elif ev.type in [xlib.KeyPress, xlib.KeyRelease]:
                # fake keyboard event data for XFilterEvent
                ev.xkey.send_event = False
                ev.xkey.window = self.replay_win

        # pass _all_ events to XFilterEvent
        filtered = bool(xlib.XFilterEvent(ev, 0))
        if ev.type == xlib.KeyRelease and \
           phantom_release(self.replay_dpy, ev.xkey):
            return
        if ev.type not in [xlib.KeyPress, xlib.KeyRelease]:
            return

        # generate new keyboard event
        data = KeyData()
        data.filtered = filtered
        data.pressed = (ev.type == xlib.KeyPress)
        data.repeated = (ev.type == last_ev.type and \
                         ev.xkey.state == last_ev.xkey.state and \
                         ev.xkey.keycode == last_ev.xkey.keycode)
        data.mods_mask = ev.xkey.state
        self._event_modifiers(ev.xkey, data)
        if not data.filtered and data.pressed and self.kbd_translate:
            self._event_keypress(ev.xkey, data)
        else:
            self._event_lookup(ev.xkey, data)
        self._event_processed(data)


    def run(self):
        # control connection
        self.control_dpy = xlib.XOpenDisplay(None)
        xlib.XSynchronize(self.control_dpy, True)

        # unmapped replay window
        self.replay_dpy = xlib.XOpenDisplay(None)
        self.custom_atom = xlib.XInternAtom(self.replay_dpy, b"SCREENKEY", False)
        replay_fd = xlib.XConnectionNumber(self.replay_dpy)
        self.replay_win = create_replay_window(self.replay_dpy)

        if self.input_types & InputType.keyboard:
            self._kbd_init()

        # initialize recording context
        ev_ranges = []
        dev_ranges = []
        if self.input_types & InputType.keyboard:
            ev_ranges.append([xlib.FocusIn, xlib.FocusOut])
            dev_ranges.append([xlib.KeyPress, xlib.KeyRelease])
        if self.input_types & InputType.button:
            dev_ranges.append([xlib.ButtonPress, xlib.ButtonRelease])
        if self.input_types & InputType.movement:
            dev_ranges.append([xlib.MotionNotify, xlib.MotionNotify])
        self.record_ctx = record_context(self.control_dpy, ev_ranges, dev_ranges);

        record_dpy = xlib.XOpenDisplay(None)
        record_fd = xlib.XConnectionNumber(record_dpy)
        # we need to keep the record_ref alive(!)
        record_ref = record_enable(record_dpy, self.record_ctx, self._event_received)

        # event loop
        last_ev = xlib.XEvent()
        self.lock.release()
        while True:
            with self.lock:
                if self.stopped:
                    break

            r_fd = []
            if xlib.XPending(record_dpy):
                r_fd.append(record_fd)
            if xlib.XPending(self.replay_dpy):
                r_fd.append(replay_fd)
            if not r_fd:
                r_fd, _, _ = select.select([record_fd, replay_fd], [], [])
            if not r_fd:
                break

            if record_fd in r_fd:
                xlib.XRecordProcessReplies(record_dpy)
                xlib.XFlush(self.replay_dpy)

            if replay_fd in r_fd:
                ev = xlib.XEvent()
                xlib.XNextEvent(self.replay_dpy, xlib.byref(ev))
                if self.input_types & InputType.keyboard:
                    self._kbd_process(ev, last_ev)
                last_ev = ev

        # finalize
        xlib.XRecordFreeContext(self.control_dpy, self.record_ctx)
        xlib.XCloseDisplay(self.control_dpy)
        xlib.XCloseDisplay(record_dpy)
        del record_ref

        if self.input_types & InputType.keyboard:
            self._kbd_del()

        xlib.XDestroyWindow(self.replay_dpy, self.replay_win)
        xlib.XCloseDisplay(self.replay_dpy)



if __name__ == '__main__':
    def callback(data):
        values = {}
        for k in dir(data):
            if k[0] == '_': continue
            values[k] = getattr(data, k)
        print(values)

    glib.threads_init()
    kl = InputListener(callback)
    try:
        kl.start()
        glib.MainLoop().run()
    except KeyboardInterrupt:
        pass
    kl.stop()
    kl.join()
