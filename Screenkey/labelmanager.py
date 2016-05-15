# -*- coding: utf-8 -*-
# "screenkey" is distributed under GNU GPLv3+, WITHOUT ANY WARRANTY.
# Copyright(c) 2010-2012: Pablo Seminario <pabluk@gmail.com>
# Copyright(c) 2015-2016: wave++ "Yuri D'Elia" <wavexx@thregr.org>.

from __future__ import print_function, unicode_literals, absolute_import, generators

from .keylistener import KeyListener
import glib

from collections import namedtuple
from datetime import datetime

# Key replacement data:
#
# bk_stop: stops backspace processing in baked mode, but not full mode
#          these keys generally move the caret, and are also padded with a thin space
# silent:  always stops backspace processing (baked/full mode)
#          these keys generally do not emit output in the text and cannot be processed
# spaced:  strong spacing is required around the symbol

ReplData = namedtuple('ReplData', ['value', 'font'])
KeyRepl  = namedtuple('KeyRepl',  ['bk_stop', 'silent', 'spaced', 'repl'])
KeyData  = namedtuple('KeyData',  ['stamp', 'is_ctrl', 'bk_stop', 'silent', 'spaced', 'markup'])

REPLACE_SYMS = {
    # Regular keys
    'Escape':       KeyRepl(True,  True,  True,  _('Esc')),
    'Tab':          KeyRepl(True,  False, False, _('↹')),
    'Return':       KeyRepl(True,  False, False, _('⏎')),
    'space':        KeyRepl(False, False, False, _('␣')),
    'BackSpace':    KeyRepl(True,  True,  False, _('⌫')),
    'Caps_Lock':    KeyRepl(True,  True,  True,  _('Caps')),
    'F1':           KeyRepl(True,  True,  True,  _('F1')),
    'F2':           KeyRepl(True,  True,  True,  _('F2')),
    'F3':           KeyRepl(True,  True,  True,  _('F3')),
    'F4':           KeyRepl(True,  True,  True,  _('F4')),
    'F5':           KeyRepl(True,  True,  True,  _('F5')),
    'F6':           KeyRepl(True,  True,  True,  _('F6')),
    'F7':           KeyRepl(True,  True,  True,  _('F7')),
    'F8':           KeyRepl(True,  True,  True,  _('F8')),
    'F9':           KeyRepl(True,  True,  True,  _('F9')),
    'F10':          KeyRepl(True,  True,  True,  _('F10')),
    'F11':          KeyRepl(True,  True,  True,  _('F11')),
    'F12':          KeyRepl(True,  True,  True,  _('F12')),
    'Up':           KeyRepl(True,  True,  False, _('↑')),
    'Left':         KeyRepl(True,  True,  False, _('←')),
    'Right':        KeyRepl(True,  True,  False, _('→')),
    'Down':         KeyRepl(True,  True,  False, _('↓')),
    'Prior':        KeyRepl(True,  True,  True,  _('PgUp')),
    'Next':         KeyRepl(True,  True,  True,  _('PgDn')),
    'Home':         KeyRepl(True,  True,  True,  _('Home')),
    'End':          KeyRepl(True,  True,  True,  _('End')),
    'Insert':       KeyRepl(False, True,  True,  _('Ins')),
    'Delete':       KeyRepl(True,  False, True,  _('Del')),
    'KP_End':       KeyRepl(False, False, True,  _('(1)')),
    'KP_Down':      KeyRepl(False, False, True,  _('(2)')),
    'KP_Next':      KeyRepl(False, False, True,  _('(3)')),
    'KP_Left':      KeyRepl(False, False, True,  _('(4)')),
    'KP_Begin':     KeyRepl(False, False, True,  _('(5)')),
    'KP_Right':     KeyRepl(False, False, True,  _('(6)')),
    'KP_Home':      KeyRepl(False, False, True,  _('(7)')),
    'KP_Up':        KeyRepl(False, False, True,  _('(8)')),
    'KP_Prior':     KeyRepl(False, False, True,  _('(9)')),
    'KP_Insert':    KeyRepl(False, False, True,  _('(0)')),
    'KP_Delete':    KeyRepl(False, False, True,  _('(.)')),
    'KP_Add':       KeyRepl(False, False, True,  _('(+)')),
    'KP_Subtract':  KeyRepl(False, False, True,  _('(-)')),
    'KP_Multiply':  KeyRepl(False, False, True,  _('(*)')),
    'KP_Divide':    KeyRepl(False, False, True,  _('(/)')),
    'KP_Enter':     KeyRepl(True,  False, False, _('⏎')),
    'Num_Lock':     KeyRepl(False, True,  True,  _('NumLck')),
    'Scroll_Lock':  KeyRepl(False, True,  True,  _('ScrLck')),
    'Pause':        KeyRepl(False, True,  True,  _('Pause')),
    'Break':        KeyRepl(False, True,  True,  _('Break')),
    'Print':        KeyRepl(False, True,  True,  _('Print')),
    'Multi_key':    KeyRepl(False, True,  True,  _('Compose')),

    # Multimedia keys
    'XF86AudioMute':         KeyRepl(True, True, True, [ReplData(_('\uf026'), 'FontAwesome'),
                                                        ReplData(_('Mute'),    None)]),
    'XF86AudioMicMute':      KeyRepl(True, True, True, [ReplData(_('\uf131'), 'FontAwesome'),
                                                        ReplData(_('Rec'),     None)]),
    'XF86AudioRaiseVolume':  KeyRepl(True, True, True, [ReplData(_('\uf028'), 'FontAwesome'),
                                                        ReplData(_('Vol+'),    None)]),
    'XF86AudioLowerVolume':  KeyRepl(True, True, True, [ReplData(_('\uf027'), 'FontAwesome'),
                                                        ReplData(_('Vol-'),    None)]),
    'XF86MonBrightnessDown': KeyRepl(True, True, True, [ReplData(_('\uf186'), 'FontAwesome'),
                                                        ReplData(_('Bright+'), None)]),
    'XF86MonBrightnessUp':   KeyRepl(True, True, True, [ReplData(_('\uf185'), 'FontAwesome'),
                                                        ReplData(_('Bright-'), None)]),
    'XF86Display':           KeyRepl(True, True, True, [ReplData(_('\uf108'), 'FontAwesome'),
                                                        ReplData(_('Display'), None)]),
    'XF86WLAN':              KeyRepl(True, True, True, [ReplData(_('\uf1eb'), 'FontAwesome'),
                                                        ReplData(_('WLAN'),    None)]),
    'XF86Search':            KeyRepl(True, True, True, [ReplData(_('\uf002'), 'FontAwesome'),
                                                        ReplData(_('Search'),  None)]),
}

WHITESPACE_SYMS = set(['Tab', 'Return', 'space', 'KP_Enter'])

MODS_MAP = {
    'normal': 0,
    'emacs': 1,
    'mac': 2,
}

MODS_SYMS = {
    'shift':  {'Shift_L', 'Shift_R'},
    'ctrl':   {'Control_L', 'Control_R'},
    'alt':    {'Alt_L', 'Alt_R', 'Meta_L', 'Meta_R'},
    'super':  {'Super_L', 'Super_R'},
    'hyper':  {'Hyper_L', 'Hyper_R'},
    'alt_gr': {'ISO_Level3_Shift'},
}

REPLACE_MODS = {
    'shift':  (_('Shift+'), 'S-',     _('⇧+')),
    'ctrl':   (_('Ctrl+'),  'C-',     _('⌘+')),
    'alt':    (_('Alt+'),   'M-',     _('⌥+')),
    'super':  (_('Super+'), 's-',     _('Super+')),
    'hyper':  (_('Hyper+'), 'H-',     _('Hyper+')),
    'alt_gr': (_('AltGr+'), 'AltGr-', _('AltGr+')),
}


def keysym_to_mod(keysym):
    for k, v in MODS_SYMS.items():
        if keysym in v:
            return k
    return None


class LabelManager(object):
    def __init__(self, listener, logger, key_mode, bak_mode, mods_mode, mods_only,
                 multiline, vis_shift, vis_space, recent_thr, compr_cnt, ignore, pango_ctx):
        self.key_mode = key_mode
        self.bak_mode = bak_mode
        self.mods_mode = mods_mode
        self.mods_index = MODS_MAP[mods_mode]
        self.logger = logger
        self.listener = listener
        self.data = []
        self.enabled = True
        self.mods_only = mods_only
        self.multiline = multiline
        self.vis_shift = vis_shift
        self.vis_space = vis_space
        self.recent_thr = recent_thr
        self.compr_cnt = compr_cnt
        self.ignore = ignore
        self.kl = None
        self.font_families = {x.get_name() for x in pango_ctx.list_families()}
        self.update_replacement_map()


    def __del__(self):
        self.stop()


    def start(self):
        self.stop()
        compose = (self.key_mode == 'composed')
        translate = (self.key_mode in ['composed', 'translated'])
        self.kl = KeyListener(self.key_press, compose, translate)
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


    def get_repl_markup(self, repl):
        if type(repl) != list:
            repl = [repl]
        for c in repl:
            if type(c) != ReplData:
                return unicode(glib.markup_escape_text(c))
            if c.font is None:
                return unicode(glib.markup_escape_text(c.value))
            elif c.font in self.font_families:
                return '<span font_family="' + c.font + '">' + \
                    unicode(glib.markup_escape_text(c.value)) + '</span>'

    def update_replacement_map(self):
        self.replace_syms = {}
        for k, v in REPLACE_SYMS.items():
            markup = self.get_repl_markup(v.repl)
            self.replace_syms[k] = KeyRepl(v.bk_stop, v.silent, v.spaced, markup)


    def update_text(self):
        markup = ""
        recent = False
        stamp = datetime.now()
        repeats = 0
        for i, key in enumerate(self.data):
            if i != 0:
                last = self.data[i - 1]

                # compress repeats
                if self.compr_cnt and key.markup == last.markup:
                    repeats += 1
                    if repeats < self.compr_cnt:
                        pass
                    elif i == len(self.data) - 1 or key.markup != self.data[i + 1].markup:
                        if not recent and (stamp - key.stamp).total_seconds() < self.recent_thr:
                            markup += '<u>'
                            recent = True
                        markup += '<sub><small>…{}×</small></sub>'.format(repeats + 1)
                        if len(key.markup) and key.markup[-1] == '\n':
                            markup += '\n'
                        continue
                    else:
                        continue

                # character block spacing
                if len(last.markup) and last.markup[-1] == '\n':
                    pass
                elif key.is_ctrl or last.is_ctrl or key.spaced or last.spaced:
                    markup += ' '
                elif key.bk_stop or last.bk_stop or repeats > self.compr_cnt:
                    markup += '<span font_family="sans">\u2009</span>'
                if key.markup != last.markup:
                    repeats = 0

            key_markup = key.markup
            if not recent and (stamp - key.stamp).total_seconds() < self.recent_thr:
                recent = True
                key_markup = '<u>' + key_markup

            # disable ligatures
            if len(key.markup) == 1 and 0x0300 <= ord(key.markup) <= 0x036F:
                # workaround for pango not handling ZWNJ correctly for combining marks
                markup += '\u180e' + key_markup + '\u200a'
            elif len(key_markup):
                markup += '\u200c' + key_markup

        if len(markup) and markup[-1] == '\n':
            markup = markup.rstrip('\n')
            if not self.vis_space and not self.data[-1].is_ctrl:
                # always show some return symbol at the last line
                markup += self.replace_syms['Return'].repl
        if recent:
            markup += '</u>'
        self.logger.debug("Label updated: %s." % repr(markup))
        self.listener(markup)


    def key_press(self, event):
        if event.pressed == False:
            self.logger.debug("Key released {:5}(ks): {}".format(event.keysym, event.symbol))
            return
        if event.symbol in self.ignore:
            self.logger.debug("Key ignored  {:5}(ks): {}".format(event.keysym, event.symbol))
            return
        if event.filtered:
            self.logger.debug("Key filtered {:5}(ks): {}".format(event.keysym, event.symbol))
        else:
            state = "repeated" if event.repeated else "pressed"
            string = repr(event.string)
            self.logger.debug("Key {:8} {:5}(ks): {} ({}, mask: {:08b})".format
                              (state, event.keysym, string, event.symbol, event.mods_mask))

        # Enable/disable handling
        if not event.repeated and event.modifiers['ctrl'] \
           and event.symbol in MODS_SYMS['ctrl']:
            self.enabled = not self.enabled
            self.logger.info("Ctrl+Ctrl detected: screenkey %s." %
                             ('enabled' if self.enabled else 'disabled'))
        if not self.enabled:
            return False

        # keep the window alive as the user is composing
        mod_pressed = keysym_to_mod(event.symbol) is not None
        update = len(self.data) and (event.filtered or mod_pressed)

        if not event.filtered:
            if self.key_mode in ['translated', 'composed']:
                update |= self.key_normal_mode(event)
            elif self.key_mode == 'raw':
                update |= self.key_raw_mode(event)
            else:
                update |= self.key_keysyms_mode(event)
        if update:
            self.update_text()


    def key_normal_mode(self, event):
        # Visible modifiers
        mod = ''
        for cap in ['ctrl', 'alt', 'super', 'hyper']:
            if event.modifiers[cap]:
                mod = mod + REPLACE_MODS[cap][self.mods_index]

        # Backspace handling
        if event.symbol == 'BackSpace' and not self.mods_only and \
           mod == '' and not event.modifiers['shift']:
            key_repl = self.replace_syms.get(event.symbol)
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
        key_repl = self.replace_syms.get(event.symbol)
        replaced = key_repl is not None
        if key_repl is None:
            if keysym_to_mod(event.symbol):
                return False
            else:
                repl = event.string or event.symbol
                markup = unicode(glib.markup_escape_text(repl))
                key_repl = KeyRepl(False, False, len(repl) > 1, markup)

        if event.modifiers['shift'] and \
           (replaced or (mod != '' and \
                         self.vis_shift and \
                         self.mods_mode != 'emacs')):
            # add back shift for translated keys
            mod = mod + REPLACE_MODS['shift'][self.mods_index]

        # Whitespace handling
        if not self.vis_space and mod == '' and event.symbol in WHITESPACE_SYMS:
            if event.symbol not in ['Return', 'KP_Enter']:
                repl = event.string
            elif self.multiline:
                repl = ''
            else:
                repl = key_repl.repl
            key_repl = KeyRepl(key_repl.bk_stop, key_repl.silent, key_repl.spaced, repl)

        # Multiline
        if event.symbol in ['Return', 'KP_Enter'] and self.multiline == True:
            key_repl = KeyRepl(key_repl.bk_stop, key_repl.silent,
                               key_repl.spaced, key_repl.repl + '\n')

        if mod == '':
            if not self.mods_only:
                repl = key_repl.repl

                # switches
                if event.symbol in ['Caps_Lock', 'Num_Lock']:
                    state = event.modifiers[event.symbol.lower()]
                    repl += '(%s)' % (_('off') if state else _('on'))

                self.data.append(KeyData(datetime.now(), False, key_repl.bk_stop,
                                         key_repl.silent, key_repl.spaced, repl))
                return True
        else:
            if self.mods_mode == 'emacs' or key_repl.repl[0] != mod[-1]:
                repl = mod + key_repl.repl
            else:
                repl = mod + '‟' + key_repl.repl + '”'
            self.data.append(KeyData(datetime.now(), True, key_repl.bk_stop,
                                     key_repl.silent, key_repl.spaced, repl))
            return True

        return False


    def key_raw_mode(self, event):
        # modifiers
        mod = ''
        for cap in REPLACE_MODS.keys():
            if event.modifiers[cap]:
                mod = mod + REPLACE_MODS[cap][self.mods_index]

        # keycaps
        key_repl = self.replace_syms.get(event.symbol)
        if key_repl is None:
            if keysym_to_mod(event.symbol):
                return False
            else:
                repl = event.string.upper() if event.string else event.symbol
                markup = unicode(glib.markup_escape_text(repl))
                key_repl = KeyRepl(False, False, len(repl) > 1, markup)

        if mod == '':
            repl = key_repl.repl

            # switches
            if event.symbol in ['Caps_Lock', 'Num_Lock']:
                state = event.modifiers[event.symbol.lower()]
                repl += '(%s)' % (_('off') if state else _('on'))

            self.data.append(KeyData(datetime.now(), False, key_repl.bk_stop,
                                     key_repl.silent, key_repl.spaced, repl))
        else:
            if self.mods_mode == 'emacs' or key_repl.repl[0] != mod[-1]:
                repl = mod + key_repl.repl
            else:
                repl = mod + '‟' + key_repl.repl + '”'
            self.data.append(KeyData(datetime.now(), True, key_repl.bk_stop,
                                     key_repl.silent, key_repl.spaced, repl))
        return True


    def key_keysyms_mode(self, event):
        if event.symbol in REPLACE_SYMS:
            value = event.symbol
        else:
            value = event.string or event.symbol
        self.data.append(KeyData(datetime.now(), True, True, True, True, value))
        return True
