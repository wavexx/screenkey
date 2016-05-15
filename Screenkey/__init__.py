import gettext
gettext.install('screenkey', unicode=True)

# Screenkey version
APP_NAME = "Screenkey"
APP_DESC = _("Screencast your keys")
APP_URL = 'http://www.thregr.org/~wavexx/software/screenkey/'
VERSION = '0.9'

# CLI/Interface options
POSITIONS = {
    'top': _('Top'),
    'center': _('Center'),
    'bottom': _('Bottom'),
    'fixed': _('Fixed'),
}

FONT_SIZES = {
    'large': _('Large'),
    'medium': _('Medium'),
    'small': _('Small'),
}

KEY_MODES = {
    'composed': _('Composed'),
    'translated': _('Translated'),
    'keysyms': _('Keysyms'),
    'raw': _('Raw'),
}

BAK_MODES = {
    'normal': _('Normal'),
    'baked': _('Baked'),
    'full': _('Full'),
}

MODS_MODES = {
    'normal': _('Normal'),
    'emacs': _('Emacs'),
    'mac': _('Mac'),
}

class Options(dict):
    def __getattr__(self, k):
        return self[k]

    def __setattr__(self, k, v):
        self[k] = v
