# -*- coding: utf-8 -*-
# "screenkey" is distributed under GNU GPLv3+, WITHOUT ANY WARRANTY.
# Copyright(c) 2010-2012 Pablo Seminario <pabluk@gmail.com>
# Copyright(c) 2015 by wave++ "Yuri D'Elia" <wavexx@thregr.org>.

from __future__ import print_function, unicode_literals, division

import os
import re
import subprocess


def cmd_keymap_table():
    proc = subprocess.Popen(['xmodmap', '-pk'],
                            stdout=subprocess.PIPE,
                            env={'DISPLAY': os.environ.get('DISPLAY'),
                                 'XAUTHORITY': os.environ.get('XAUTHORITY'),
                                 'LC_ALL': 'C'})
    return proc.communicate()[0]


def cmd_modifier_map():
    proc = subprocess.Popen(['xmodmap', '-pm'],
                            stdout=subprocess.PIPE,
                            env={'DISPLAY': os.environ.get('DISPLAY'),
                                 'XAUTHORITY': os.environ.get('XAUTHORITY'),
                                 'LC_ALL': 'C'})
    return proc.communicate()[0]


def get_keymap_table():
    keymap = {}
    keymap_table = cmd_keymap_table()

    re_line = re.compile(r'0x\w+')
    for line in keymap_table.split('\n')[1:]:
        if len(line) > 0:
            keycode = re.search(r'\s+(\d+).*', line)
            if keycode:
                new_keysyms = []
                keycode = int(keycode.group(1))
                keysyms = re_line.findall(line)

                # When you press only one key
                unicode_char = ''
                try:
                    unicode_char = unichr(int(keysyms[0], 16))
                except:
                    unicode_char = ''
                if unicode_char == '\x00':
                    unicode_char = ''
                new_keysyms.append(unicode_char)

                # When you press a key plus Shift key
                unicode_char = ''
                try:
                    unicode_char = unichr(int(keysyms[1], 16))
                except:
                    unicode_char = ''
                if unicode_char == '\x00':
                    unicode_char = ''
                new_keysyms.append(unicode_char)

                # When you press a key plus meta (dead keys)
                unicode_char = ''
                try:
                    unicode_char = unichr(int(keysyms[4], 16))
                except:
                    unicode_char = ''
                if unicode_char == '\x00':
                    unicode_char = ''
                new_keysyms.append(unicode_char)

                # When you press a key plus meta plus Shift key
                unicode_char = ''
                try:
                    unicode_char = unichr(int(keysyms[5], 16))
                except:
                    unicode_char = ''
                if unicode_char == '\x00':
                    unicode_char = ''
                new_keysyms.append(unicode_char)

                keymap[keycode] = new_keysyms

    return keymap


def get_modifier_map():
    modifiers = {}
    modifier_map = cmd_modifier_map()
    re_line = re.compile(r'(0x\w+)')

    for line in modifier_map.split('\n')[1:]:
        if len(line) > 0:
            mod_name = re.match(r'(\w+).*', line)
            if mod_name:
                mod_name = mod_name.group(1)
                keycodes = re_line.findall(line)

                # Convert key codes from hex to dec for use them
                # with the keymap table
                keycodes = [int(kc, 16) for kc in keycodes]

                modifiers[mod_name] = keycodes

    return modifiers
