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
else:
    from . import xlib

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
def record_context(dpy, ev_range):
    range_spec = xlib.XRecordAllocRange()
    range_spec.contents.device_events.first = ev_range[0]
    range_spec.contents.device_events.last = ev_range[1]
    rec_ctx = xlib.XRecordCreateContext(
        dpy, 0,
        xlib.byref(xlib.c_ulong(xlib.XRecordAllClients)), 1,
        xlib.byref(range_spec), 1)
    xlib.XFree(range_spec)
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



class KeyData():
    def __init__(self, filtered=None, string=None, keysym=None, status=None,
                 symbol=None, mods_mask=None, modifiers=None):
        self.filtered = filtered
        self.string = string
        self.keysym = keysym
        self.status = status
        self.symbol = symbol
        self.mods_mask = mods_mask
        self.modifiers = modifiers


class KeyListener(threading.Thread):
    def __init__(self, callback, mode):
        super(KeyListener, self).__init__()
        self.callback = callback
        self.mode = mode
        self._lock = threading.Lock()
        self._stop = True


    def _event_received(self, ev):
        if ev.type in [xlib.KeyPress, xlib.KeyRelease]:
            xlib.XSendEvent(self.replay_dpy, self.replay_win, False, 0, ev)
        elif ev.type in [xlib.FocusIn, xlib.FocusOut]:
            xlib.XFree(xlib.Xutf8ResetIC(self.replay_xic))
        xlib.XFlush(self.replay_dpy)


    def _event_callback(self, data):
        self.callback(data)
        return False

    def _event_processed(self, data):
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
        modifiers['mode_switch'] = bool(kev.state & xlib.Mod5Mask)


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
        data.symbol = xlib.XKeysymToString(keysym)


    def start(self):
        self._lock.acquire()
        self._stop = False
        super(KeyListener, self).start()


    def stop(self):
        with self._lock:
            if not self._stop:
                self._stop = True
                xlib.XRecordDisableContext(self.control_dpy, self.record_ctx)


    def run(self):
        self.control_dpy = xlib.XOpenDisplay(None)
        xlib.XSynchronize(self.control_dpy, True)
        self.record_ctx = record_context(self.control_dpy, [xlib.KeyPress, xlib.FocusOut])
        record_dpy = xlib.XOpenDisplay(None)
        record_fd = xlib.XConnectionNumber(record_dpy)

        # note that we never ever map the window
        self.replay_dpy = xlib.XOpenDisplay(None)
        replay_fd = xlib.XConnectionNumber(self.replay_dpy)
        self.replay_win = create_replay_window(self.replay_dpy)

        if self.mode == 'raw':
            style = xlib.XIMPreeditNone | xlib.XIMStatusNone
        else:
            style = xlib.XIMPreeditNothing | xlib.XIMStatusNothing

        replay_xim = xlib.XOpenIM(self.replay_dpy, None, None, None)
        self.replay_xic = xlib.XCreateIC(replay_xim,
                                         xlib.XNClientWindow, self.replay_win,
                                         xlib.XNInputStyle, style,
                                         None)
        xlib.XSetICFocus(self.replay_xic)

        # we need to keep the proc_ref alive
        proc_ref = record_enable(record_dpy, self.record_ctx, self._event_received)

        self._lock.release()
        while True:
            with self._lock:
                if self._stop:
                    break
            r_fd, _, _ = select.select([record_fd, replay_fd], [], [])
            if not r_fd:
                break

            if record_fd in r_fd:
                xlib.XRecordProcessReplies(record_dpy)

            if replay_fd in r_fd:
                ev = xlib.XEvent()
                xlib.XNextEvent(self.replay_dpy, xlib.byref(ev))
                ev.xkey.send_event = False
                ev.xkey.window = self.replay_win

                data = KeyData()
                data.filtered = xlib.XFilterEvent(ev, 0)
                data.mods_mask = ev.xkey.state
                self._event_modifiers(ev.xkey, data)

                if data.filtered:
                    # still signal to the receiver that the raw event was filtered
                    self._event_processed(data)
                    continue

                if ev.type == xlib.KeyPress:
                    self._event_keypress(ev.xkey, data)
                    self._event_processed(data)
                    continue

        xlib.XRecordFreeContext(self.control_dpy, self.record_ctx)
        xlib.XCloseDisplay(self.control_dpy)
        xlib.XCloseDisplay(record_dpy)
        del proc_ref

        xlib.XDestroyIC(self.replay_xic)
        xlib.XCloseIM(replay_xim)
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
    kl = KeyListener(callback, 'normal')
    try:
        kl.start()
        glib.MainLoop().run()
    except KeyboardInterrupt:
        pass
    kl.stop()
    kl.join()
