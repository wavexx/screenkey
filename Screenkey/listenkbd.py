# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Pablo Seminario <pabluk@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function, unicode_literals, division

from . import modmap

import pygtk, gtk
pygtk.require('2.0')

import sys
import threading
from collections import namedtuple

from Xlib import X, XK, display
from Xlib.ext import record
from Xlib.protocol import rq


KeyRepl = namedtuple('KeyRepl', ['bk_stop', 'repl'])
KeyData = namedtuple('KeyData', ['is_ctrl', 'bk_stop', 'repl'])

REPLACE_KEYS = {
    'XK_Escape':        KeyRepl(True,  _('Esc')),
    'XK_Tab':           KeyRepl(True,  '↹'),
    'XK_Return':        KeyRepl(True,  '⏎'),
    'XK_space':         KeyRepl(False, '␣'),
    'XK_BackSpace':     KeyRepl(True,  '⌫'),
    'XK_Caps_Lock':     KeyRepl(False, _('Caps')),
    'XK_F1':            KeyRepl(True,  'F1'),
    'XK_F2':            KeyRepl(True,  'F2'),
    'XK_F3':            KeyRepl(True,  'F3'),
    'XK_F4':            KeyRepl(True,  'F4'),
    'XK_F5':            KeyRepl(True,  'F5'),
    'XK_F6':            KeyRepl(True,  'F6'),
    'XK_F7':            KeyRepl(True,  'F7'),
    'XK_F8':            KeyRepl(True,  'F8'),
    'XK_F9':            KeyRepl(True,  'F9'),
    'XK_F10':           KeyRepl(True,  'F10'),
    'XK_F11':           KeyRepl(True,  'F11'),
    'XK_F12':           KeyRepl(True,  'F12'),
    'XK_Home':          KeyRepl(True,  _('Home')),
    'XK_Up':            KeyRepl(True,  '↑'),
    'XK_Page_Up':       KeyRepl(True,  _('PgUp')),
    'XK_Left':          KeyRepl(True,  '←'),
    'XK_Right':         KeyRepl(True,  '→'),
    'XK_End':           KeyRepl(True,  _('End')),
    'XK_Down':          KeyRepl(True,  '↓'),
    'XK_Next':          KeyRepl(True,  _('PgDn')),
    'XK_Insert':        KeyRepl(False, _('Ins')),
    'XK_Delete':        KeyRepl(True,  _('Del')),
    'XK_KP_Home':       KeyRepl(False, '(7)'),
    'XK_KP_Up':         KeyRepl(False, '(8)'),
    'XK_KP_Prior':      KeyRepl(False, '(9)'),
    'XK_KP_Left':       KeyRepl(False, '(4)'),
    'XK_KP_Right':      KeyRepl(False, '(6)'),
    'XK_KP_End':        KeyRepl(False, '(1)'),
    'XK_KP_Down':       KeyRepl(False, '(2)'),
    'XK_KP_Page_Down':  KeyRepl(False, '(3)'),
    'XK_KP_Begin':      KeyRepl(False, '(5)'),
    'XK_KP_Insert':     KeyRepl(False, '(0)'),
    'XK_KP_Delete':     KeyRepl(False, '(.)'),
    'XK_KP_Add':        KeyRepl(False, '(+)'),
    'XK_KP_Subtract':   KeyRepl(False, '(-)'),
    'XK_KP_Multiply':   KeyRepl(False, '(*)'),
    'XK_KP_Divide':     KeyRepl(False, '(/)'),
    'XK_Num_Lock':      KeyRepl(False, 'NumLock'),
    'XK_KP_Enter':      KeyRepl(True,  '⏎'),
}

MODS_EVENT_MASK = {
    'shift': gtk.gdk.SHIFT_MASK,
    'lock': gtk.gdk.LOCK_MASK,
    'ctrl': gtk.gdk.CONTROL_MASK,
    'alt': gtk.gdk.MOD1_MASK,
    'mod2': gtk.gdk.MOD2_MASK,
    'mod3': gtk.gdk.MOD3_MASK,
    'super': gtk.gdk.MOD4_MASK,
    'hyper': gtk.gdk.MOD5_MASK,
}

MODS_MAP = {
    'normal': 0,
    'emacs': 1,
    'mac': 2,
}

REPLACE_MODS = {
    'shift': (_('Shift+'),   'S-', '⇧+'),
    'ctrl':  (_('Control+'), 'C-', '⌘+'),
    'alt':   (_('Alt+'),     'M-', '⌥+'),
    'super': (_('Super+'),   's-', _('Super+')),
    'hyper': (_('Hyper+'),   'H-', _('Hyper+')),
}


class ListenKbd(threading.Thread):
    def __init__(self, listener, logger, key_mode, bak_mode, mods_mode, mods_only):
        threading.Thread.__init__(self)
        self.key_mode = key_mode
        self.bak_mode = bak_mode
        self.mods_index = MODS_MAP[mods_mode]
        self.logger = logger
        self.listener = listener
        self.data = []
        self.enabled = True
        self.mutex = threading.Lock()
        self.mods_only = mods_only
        self.cmd_keys = {mod: False for mod in MODS_EVENT_MASK.keys()}
        self.logger.debug("Thread created")
        self.keymap = modmap.get_keymap_table()
        self.modifiers = modmap.get_modifier_map()

        self.local_dpy = display.Display()
        self.record_dpy = display.Display()

        if not self.record_dpy.has_extension("RECORD"):
            self.logger.error("RECORD extension not found.")
            sys.exit(1)

        self.ctx = self.record_dpy.record_create_context(
            0, [record.AllClients],
            [{'core_requests': (0, 0),
              'core_replies': (0, 0),
              'ext_requests': (0, 0, 0, 0),
              'ext_replies': (0, 0, 0, 0),
              'delivered_events': (0, 0),
              'device_events': (X.KeyPress, X.KeyRelease),
              'errors': (0, 0),
              'client_started': False,
              'client_died': False}])


    def run(self):
        self.logger.debug("Thread started.")
        self.record_dpy.record_enable_context(self.ctx, self.key_press)
        self.record_dpy.record_free_context(self.ctx)
        self.logger.debug("Thread stopped.")


    def clear(self):
        with self.mutex:
            self.data = []


    def lookup_keysym(self, keysym):
        for name in dir(XK):
            if name[:3] == "XK_" and getattr(XK, name) == keysym:
                return name[3:]
        return keysym


    def key_repl(self, key, keysym):
        for name in dir(XK):
            if name[:3] == "XK_" and getattr(XK, name) == keysym:
                if name in REPLACE_KEYS:
                    return REPLACE_KEYS[name]


    def update_text(self):
        string = ""
        for i, key in enumerate(self.data):
            if i != 0:
                last = self.data[i - 1]
                if len(key.repl) > 1 or len(last.repl) > 1:
                    string += ' '
            string += '\u200c' + key.repl
        self.logger.debug("Label updated: %s." % string)
        self.listener(string)


    def key_press(self, reply):
        with self.mutex:
            self._key_press(reply)

    def _key_press(self, reply):
        if reply.category != record.FromServer:
            return
        if reply.client_swapped:
            self.logger.warning("received swapped protocol data, cowardly ignored")
            return
        if not len(reply.data) or ord(reply.data[0]) < 2:
            # not an event
            return

        data = reply.data
        update = False
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data,
                                    self.record_dpy.display, None, None)
            if event.type in [X.KeyPress, X.KeyRelease]:
                self.process_modifiers(event)
                if not self.process_enabled(event):
                    continue
                if self.key_mode == 'normal':
                    update |= self.key_normal_mode(event) or False
                else:
                    update |= self.key_raw_mode(event) or False
        if update:
            self.update_text()


    def process_enabled(self, event):
        if event.type == X.KeyPress:
            if event.detail in self.modifiers['control'] and self.cmd_keys['ctrl']:
                self.enabled = not self.enabled
                self.logger.info("Ctrl+Ctrl detected: screenkey %s." %
                                 'enabled' if self.enabled else 'disabled')
        return self.enabled


    def process_modifiers(self, event):
        for mod, mask in MODS_EVENT_MASK.iteritems():
            self.cmd_keys[mod] = event.state & mask


    def key_normal_mode(self, event):
        keysym = self.local_dpy.keycode_to_keysym(event.detail, 0)
        if event.detail in self.keymap:
            key_normal, key_shift, key_dead, key_deadshift = self.keymap[event.detail]
            self.logger.debug(
                "Key %s(keycode) %s. Symbols %s" %
                (event.detail, event.type == X.KeyPress and "pressed" or "released",
                 self.keymap[event.detail]))
        else:
            self.logger.debug('No mapping for scan_code %d' % event.detail)
            return

        # Ignore direct modifier keypresses
        for kcs in self.modifiers.values():
            if event.detail in kcs:
                return

        # Backspace key
        if event.detail == 22 and event.type == X.KeyPress and \
          not any(self.cmd_keys.values()) and not self.mods_only:
            key_repl = self.key_repl(key_normal, keysym)
            if self.bak_mode == 'normal':
                self.data.append(KeyData(False, *key_repl))
                return True
            else:
                if len(self.data) and self.data[-1].repl != key_repl.repl and \
                   not self.data[-1].is_ctrl and (self.bak_mode == 'full' or not self.data[-1].bk_stop):
                    self.data.pop()
                else:
                    self.data.append(KeyData(False, *key_repl))
                return True

        # Regular keys
        if event.type == X.KeyPress:
            key = key_normal

            # visible modifiers
            mod = ''
            for cap in ['ctrl', 'alt', 'super', 'hyper']:
                if self.cmd_keys[cap]:
                    mod = mod + REPLACE_MODS[cap][self.mods_index]

            # silent modifiers
            if self.cmd_keys['shift']:
                key = key_shift
            if self.cmd_keys['lock'] and ord(key_normal) in range(97, 123):
                key = key_shift
            if self.cmd_keys['hyper']:
                key = key_dead
            if self.cmd_keys['shift'] and self.cmd_keys['hyper']:
                key = key_deadshift

            key_repl = self.key_repl(key, keysym)
            if key_repl is None:
                key_repl = KeyRepl(False, key)
            elif self.cmd_keys['shift']:
                # add back shift for translated keys
                mod = mod + REPLACE_MODS['shift'][self.mods_index]

            if mod == '':
                if not self.mods_only:
                    self.data.append(KeyData(False, *key_repl))
                    return True
            else:
                repl = mod + key_repl.repl
                self.data.append(KeyData(True, key_repl.bk_stop, repl))
                return True

        # Ignore anything else
        return False


    def key_raw_mode(self, event):
        if event.type == X.KeyPress:
            keysym = self.local_dpy.keycode_to_keysym(event.detail, 0)
            key = self.lookup_keysym(keysym)
            self.data.append(KeyRepl(True, key))
            return True


    def stop(self):
        self.local_dpy.record_disable_context(self.ctx)
        self.local_dpy.flush()
