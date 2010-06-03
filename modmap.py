#!/usr/bin/env python

import re
import subprocess

def cmd_keymap_table():
    return subprocess.Popen(['xmodmap','-pk'], stdout=subprocess.PIPE).communicate()[0]

def cmd_modifier_map():
    return subprocess.Popen(['xmodmap','-pm'], stdout=subprocess.PIPE).communicate()[0]

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
                try:
                    new_keysyms.append(unichr(int(keysyms[0], 16)))
                except:
                    new_keysyms.append('')
                # When you press a key plus Shift key
                try:
                    new_keysyms.append(unichr(int(keysyms[1], 16)))
                except:
                    new_keysyms.append('')
                # When you press a key plus meta (dead keys)
                try:
                    new_keysyms.append(unichr(int(keysyms[4], 16)))
                except:
                    new_keysyms.append('')
                # When you press a key plus meta plus Shift key (dead keys)
                try:
                    new_keysyms.append(unichr(int(keysyms[5], 16)))
                except:
                    new_keysyms.append('')

    		keymap[keycode-8] = new_keysyms

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
		# range from 8 to 255 (-8)
                keycodes =[ int(kc, 16)-8 for kc in keycodes]
                
                modifiers[mod_name] = keycodes

    return modifiers

