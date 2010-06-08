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

import threading
import time
import sys
import evdev
import modmap
from devices import InputFinder

REPLACE_KEYS = {
    1:u'Esc ',
    15:u'\u21B9 ',
    28:u'\u23CE ',
    57:u' ',
    58:u'Caps ',
    59:u'F1 ', 
    60:u'F2 ', 
    61:u'F3 ', 
    62:u'F4 ', 
    63:u'F5 ', 
    64:u'F6 ', 
    65:u'F7 ', 
    66:u'F8 ', 
    67:u'F9 ', 
    68:u'F10 ', 
    87:u'F11 ', 
    88:u'F12 ', 
    99:u'', 
    102:u'Home ',
    103:u'\u2191',
    104:u'PgUp ',
    105:u'\u2190',
    106:u'\u2192',
    107:u'End ',
    108:u'\u2193',
    109:u'PgDn ',
    110:u'Ins ',
    111:u'Del ',
    127:u'',
}

class ListenKbd(threading.Thread):

    stopEvent = threading.Event()

    def __init__(self, label):
        threading.Thread.__init__(self)
        self.label = label
        self.text = ""
        self.timer = None
        self.command = None
        self.shift = None
        self.cmd_keys = {
            'shift': False,
            'ctrl': False,
            'alt': False,
            'capslock': False,
            'meta': False,
            'super':False
            }


        finder = InputFinder()
        finder.connect('keyboard-found', self.DeviceFound)
        finder.connect('keyboard-lost', self.DeviceLost)

        try:
            nodes = [x.block for x in finder.keyboards.values()]
            self.devices = evdev.DeviceGroup(nodes)
        except OSError, e:
            print
            print 'You may need to run this as %r' % 'sudo %s' % sys.argv[0]
            sys.exit(-1)

        self.keymap = modmap.get_keymap_table()
        self.modifiers = modmap.get_modifier_map()


    def update_text(self, string=None):
        if not string is None:
            self.text = "%s%s" % (self.label.get_text(), string)
            self.label.set_text(self.text)
        else:
            self.label.set_text("")
        self.label.emit("text-changed")
 
    def key_press(self, event):
        code_num = event.codeMaps[event.type].toNumber(event.code)
        if code_num in self.keymap:
            key_normal, key_shift, key_dead, key_deadshift = self.keymap[code_num]
        else:
            print 'No mapping for scan_code %d' % code_num
            return

        key = ''
        mod = ''

        # Alt key
        if code_num in self.modifiers['mod1']:
            if event.value in (1, 2):
                self.cmd_keys['alt'] = True
            else:
                self.cmd_keys['alt'] = False
            return
        # Meta key 
        # Fixme: it must use self.modifiers['mod5']
        #        but doesn't work
        if code_num == 100:
            if event.value in (1, 2):
                self.cmd_keys['meta'] = True
            else:
                self.cmd_keys['meta'] = False
            return
        # Super key 
        if code_num in self.modifiers['mod4']:
            if event.value in (1, 2):
                self.cmd_keys['super'] = True
            else:
                self.cmd_keys['super'] = False
            return
        # Ctrl keys
        elif code_num in self.modifiers['control']:
            if event.value in (1, 2):
                self.cmd_keys['ctrl'] = True
            else:
                self.cmd_keys['ctrl'] = False
            return
        # Shift keys
        elif code_num in self.modifiers['shift']:
            if event.value in (1,2):
                self.cmd_keys['shift'] = True
            else:
                self.cmd_keys['shift'] = False
            return
        # Capslock key
        elif code_num in self.modifiers['lock']:
            if event.value == 1:
                if self.cmd_keys['capslock']:
                    self.cmd_keys['capslock'] = False
                else:
                    self.cmd_keys['capslock'] = True
            return
        # Backspace key
        elif code_num == 14 and event.value == 1:
            self.label.set_text(self.label.get_text()[:-1])
            key = ""
        else:
            if event.value == 1:
                key = key_normal
                if self.cmd_keys['ctrl']:
                    mod = mod + "Ctrl+"
                if self.cmd_keys['alt']:
                    mod = mod + "Alt+"
                if self.cmd_keys['super']:
                    mod = mod + "Super+"

                if self.cmd_keys['shift']:
                    key = key_shift
                if self.cmd_keys['capslock'] and ord(key_normal) in range(97,123):
                    key = key_shift
                if self.cmd_keys['meta']:
                    key = key_dead
                if self.cmd_keys['shift'] and self.cmd_keys['meta']:
                    key = key_deadshift

                if code_num in REPLACE_KEYS:
                    key = REPLACE_KEYS[code_num]
                    if not key:
                        return

                if mod != '':
                    key = "%s%s " % (mod, key)
                else:
                    key = "%s%s" % (mod, key)
            else:
                return
        self.update_text(key)

    def DeviceFound(self, finder, device):
        dev = evdev.Device(device.block)
        self.devices.devices.append(dev)
        self.devices.fds.append(dev.fd)
      
    def DeviceLost(self, finder, device):
        dev = None
        for x in self.devices.devices:
            if x.filename == device.block:
                dev = x
                break
      
        if dev:
            self.devices.fds.remove(dev.fd)
            self.devices.devices.remove(dev)

    def stop(self):
        self.stopEvent.set()
    
    def run(self):
        while not self.stopEvent.isSet():
            event = self.devices.next_event()
            if event is not None:
                if event.type == "EV_KEY":
                    if event.code.startswith("KEY"):
                        self.key_press(event)


