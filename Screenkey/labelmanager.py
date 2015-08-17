# -*- coding: utf-8 -*-
# "screenkey" is distributed under GNU GPLv3+, WITHOUT ANY WARRANTY.
# Copyright(c) 2010-2012 Pablo Seminario <pabluk@gmail.com>
# Copyright(c) 2015 by wave++ "Yuri D'Elia" <wavexx@thregr.org>.

from __future__ import print_function, unicode_literals, absolute_import

from .keylistener import KeyListener
import glib

from collections import namedtuple
from datetime import datetime

KeyRepl = namedtuple('KeyRepl', ['bk_stop', 'silent', 'repl'])
KeyData = namedtuple('KeyData', ['stamp', 'is_ctrl', 'bk_stop', 'silent', 'repl'])

REPLACE_KEYS = {
    'Escape':       KeyRepl(True,  True,  _('Esc')),
    'Tab':          KeyRepl(True,  False, _('↹')),
    'Return':       KeyRepl(True,  False, _('⏎')),
    'space':        KeyRepl(False, False, _('␣')),
    'BackSpace':    KeyRepl(True,  True,  _('⌫')),
    'Caps_Lock':    KeyRepl(True,  True,  _('Caps')),
    'F1':           KeyRepl(True,  True,  _('F1')),
    'F2':           KeyRepl(True,  True,  _('F2')),
    'F3':           KeyRepl(True,  True,  _('F3')),
    'F4':           KeyRepl(True,  True,  _('F4')),
    'F5':           KeyRepl(True,  True,  _('F5')),
    'F6':           KeyRepl(True,  True,  _('F6')),
    'F7':           KeyRepl(True,  True,  _('F7')),
    'F8':           KeyRepl(True,  True,  _('F8')),
    'F9':           KeyRepl(True,  True,  _('F9')),
    'F10':          KeyRepl(True,  True,  _('F10')),
    'F11':          KeyRepl(True,  True,  _('F11')),
    'F12':          KeyRepl(True,  True,  _('F12')),
    'Home':         KeyRepl(True,  True,  _('Home')),
    'Up':           KeyRepl(True,  True,  _('↑')),
    'Prior':        KeyRepl(True,  True,  _('PgUp')),
    'Next':         KeyRepl(True,  True,  _('PgDn')),
    'Left':         KeyRepl(True,  True,  _('←')),
    'Right':        KeyRepl(True,  True,  _('→')),
    'End':          KeyRepl(True,  True,  _('End')),
    'Down':         KeyRepl(True,  True,  _('↓')),
    'Insert':       KeyRepl(False, True,  _('Ins')),
    'Delete':       KeyRepl(True,  False, _('Del')),
    'KP_End':       KeyRepl(False, False, _('(1)')),
    'KP_Down':      KeyRepl(False, False, _('(2)')),
    'KP_Next':      KeyRepl(False, False, _('(3)')),
    'KP_Left':      KeyRepl(False, False, _('(4)')),
    'KP_Begin':     KeyRepl(False, False, _('(5)')),
    'KP_Right':     KeyRepl(False, False, _('(6)')),
    'KP_Home':      KeyRepl(False, False, _('(7)')),
    'KP_Up':        KeyRepl(False, False, _('(8)')),
    'KP_Prior':     KeyRepl(False, False, _('(9)')),
    'KP_Insert':    KeyRepl(False, False, _('(0)')),
    'KP_Delete':    KeyRepl(False, False, _('(.)')),
    'KP_Add':       KeyRepl(False, False, _('(+)')),
    'KP_Subtract':  KeyRepl(False, False, _('(-)')),
    'KP_Multiply':  KeyRepl(False, False, _('(*)')),
    'KP_Divide':    KeyRepl(False, False, _('(/)')),
    'KP_Enter':     KeyRepl(True,  False, _('⏎')),
    'Num_Lock':     KeyRepl(False, True,  _('NumLck')),
    'Scroll_Lock':  KeyRepl(False, True,  _('ScrLck')),
    'Pause':        KeyRepl(False, True,  _('Pause')),
    'Break':        KeyRepl(False, True,  _('Break')),
    'Print':        KeyRepl(False, True,  _('Print')),
    'Multi_key':    KeyRepl(False, True,  _('Compose')),
}

MODS_MAP = {
    'normal': 0,
    'emacs': 1,
    'mac': 2,
}

REPLACE_MODS = {
    'shift': (_('Shift+'), 'S-', _('⇧+')),
    'ctrl':  (_('Ctrl+'),  'C-', _('⌘+')),
    'alt':   (_('Alt+'),   'M-', _('⌥+')),
    'super': (_('Super+'), 's-', _('Super+')),
    'hyper': (_('Hyper+'), 'H-', _('Hyper+')),
}


class LabelManager(object):
    def __init__(self, listener, logger, key_mode, bak_mode, mods_mode, mods_only,
                 vis_shift, recent_thr):
        self.key_mode = key_mode
        self.bak_mode = bak_mode
        self.mods_mode = mods_mode
        self.mods_index = MODS_MAP[mods_mode]
        self.logger = logger
        self.listener = listener
        self.data = []
        self.enabled = True
        self.mods_only = mods_only
        self.vis_shift = vis_shift
        self.recent_thr = recent_thr
        self.kl = None


    def __del__(self):
        self.stop()


    def start(self):
        self.stop()
        self.kl = KeyListener(self.key_press, self.key_mode)
        self.kl.start()
        self.logger.debug("Thread started.")


    def stop(self):
        if self.kl:
            self.kl.stop()
            self.logger.debug("Thread stopped.")
            self.kl.join()
            self.kl = None


    def clear(self):
        self.data = []


    def update_text(self):
        markup = ""
        recent = False
        for i, key in enumerate(self.data):
            if i != 0:
                last = self.data[i - 1]
                if len(key.repl) > 1 or len(last.repl) > 1:
                    markup += ' '
                elif key.bk_stop or last.bk_stop:
                    markup += '<span font_family="sans">\u2009</span>'
            if not recent and (datetime.now() - key.stamp).total_seconds() < self.recent_thr:
                recent = True
                markup += '<u>'
            markup += '\u200c' + glib.markup_escape_text(key.repl)
        if recent:
            markup += '</u>'
        self.logger.debug("Label updated: %s." % repr(markup))
        self.listener(markup)


    def key_press(self, event):
        if event.pressed == False:
            self.logger.debug("Key released {:5}(ks): {}".format(event.keysym, event.symbol))
            return
        if event.filtered:
            self.logger.debug("Key filtered {:5}(ks): {}".format(event.keysym, event.symbol))
        else:
            string = "{}".format(event.string) if event.string else None
            self.logger.debug("Key pressed  {:5}(ks): {} ({}, mask: {:08b})".format
                              (event.keysym, event.string, event.symbol, event.mods_mask))

        # keep the window alive as the user is composing
        update = len(self.data) and event.filtered

        if not event.filtered:
            if self.key_mode == 'normal':
                update |= self.key_normal_mode(event)
            else:
                update |= self.key_raw_mode(event)
        if update:
            self.update_text()


    def key_normal_mode(self, event):
        # Enable/disable handling
        if event.modifiers['ctrl'] and event.symbol in ['Control_L', 'Control_R']:
            self.enabled = not self.enabled
            self.logger.info("Ctrl+Ctrl detected: screenkey %s." %
                             ('enabled' if self.enabled else 'disabled'))
        if not self.enabled:
            return False

        # Visible modifiers
        mod = ''
        for cap in ['ctrl', 'alt', 'super', 'hyper']:
            if event.modifiers[cap]:
                mod = mod + REPLACE_MODS[cap][self.mods_index]

        # Backspace handling
        if event.symbol == 'BackSpace' and mod == '' and not self.mods_only:
            key_repl = REPLACE_KEYS.get(event.symbol)
            if self.bak_mode == 'normal':
                self.data.append(KeyData(datetime.now(), False, *key_repl))
                return True
            else:
                if not len(self.data):
                    pop = False
                else:
                    last = self.data[-1]
                    if last.is_ctrl:
                        pop = False
                    elif self.bak_mode == 'baked':
                        pop = not last.bk_stop
                    else:
                        pop = not last.silent
                if pop:
                    self.data.pop()
                else:
                    self.data.append(KeyData(datetime.now(), False, *key_repl))
                return True

        # Regular keys
        key_repl = REPLACE_KEYS.get(event.symbol)
        replaced = key_repl is not None
        if key_repl is None:
            if event.string:
                key_repl = KeyRepl(False, False, event.string)
            else:
                return False
        if event.modifiers['shift'] and \
           (replaced or (mod != '' and self.vis_shift and self.mods_mode != 'emacs')):
            # add back shift for translated keys
            mod = mod + REPLACE_MODS['shift'][self.mods_index]

        if mod == '':
            if not self.mods_only:
                repl = key_repl.repl

                # switches
                if event.symbol in ['Caps_Lock', 'Num_Lock']:
                    state = event.modifiers[event.symbol.lower()]
                    repl += '(%s)' % (_('off') if state else _('on'))

                self.data.append(KeyData(datetime.now(), False, key_repl.bk_stop,
                                         key_repl.silent, repl))
        else:
            repl = mod + key_repl.repl
            self.data.append(KeyData(datetime.now(), True, key_repl.bk_stop,
                                     key_repl.silent, repl))
        return True


    def key_raw_mode(self, event):
        if event.symbol in REPLACE_KEYS:
            value = event.symbol
        else:
            value = event.string or event.symbol
        self.data.append(KeyData(datetime.now(), True, True, None, value))
        return True
