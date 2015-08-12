# -*- coding: utf-8 -*-
# "screenkey" is distributed under GNU GPLv3+, WITHOUT ANY WARRANTY.
# Copyright(c) 2010-2012 Pablo Seminario <pabluk@gmail.com>
# Copyright(c) 2015 by wave++ "Yuri D'Elia" <wavexx@thregr.org>.

from __future__ import print_function, unicode_literals, division

from . import APP_NAME, APP_DESC, APP_URL, VERSION
from .listenkbd import ListenKbd

from threading import Timer
import os
import json

import pygtk
pygtk.require('2.0')

import gtk
import glib
import pango


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
    'raw': _('Raw'),
    'normal': _('Normal'),
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


class Screenkey(gtk.Window):
    STATE_FILE = os.path.join(glib.get_user_config_dir(), 'screenkey.json')

    def __init__(self, logger, options, show_settings=False):
        gtk.Window.__init__(self)

        self.timer_hide = None
        self.timer_min = None
        self.logger = logger

        defaults = Options({'timeout': 2.5,
                            'recent_thr': 0.1,
                            'position': 'bottom',
                            'persist': False,
                            'font_desc': 'Sans Bold',
                            'font_size': 'medium',
                            'key_mode': 'normal',
                            'bak_mode': 'baked',
                            'mods_mode': 'normal',
                            'mods_only': False,
                            'geometry': None,
                            'screen': 0})
        self.options = self.load_state()
        if self.options is None:
            self.options = defaults
        else:
            # copy missing defaults
            for k, v in defaults.iteritems():
                if k not in self.options:
                    self.options[k] = v
        if options is not None:
            # override with values from constructor
            for k, v in options.iteritems():
                if v is not None:
                    self.options[k] = v

        self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_keep_above(True)
        self.set_decorated(False)
        self.stick()
        self.set_property('accept-focus', False)
        self.set_property('focus-on-map', False)
        bgcolor = gtk.gdk.color_parse("black")
        self.modify_bg(gtk.STATE_NORMAL, bgcolor)
        self.set_opacity(0.8)

        self.label = gtk.Label()
        self.label.set_attributes(pango.AttrList())
        self.label.set_ellipsize(pango.ELLIPSIZE_START)
        self.label.show()
        self.add(self.label)

        self.set_gravity(gtk.gdk.GRAVITY_CENTER)
        self.connect("configure-event", self.on_configure)
        scr = self.get_screen()
        scr.connect("size-changed", self.on_configure)
        scr.connect("monitors-changed", self.on_monitors_changed)
        self.set_active_monitor(self.options.screen)

        self.font = pango.FontDescription(self.options.font_desc)
        self.update_label()

        self.listenkbd = None
        self.on_change_mode()

        self.make_menu()
        self.make_about_dialog()
        self.make_preferences_dialog()
        self.make_systray()

        self.connect("delete-event", self.quit)
        if show_settings:
            self.on_preferences_dialog()
        if self.options.persist:
            self.show()


    def quit(self, widget, data=None):
        self.listenkbd.stop()
        gtk.main_quit()


    def load_state(self):
        """Load stored options"""
        options = None
        try:
            with open(self.STATE_FILE, 'r') as f:
                options = Options(json.load(f))
                self.logger.debug("Options loaded.")
        except IOError:
            self.logger.debug("file %s does not exists." % self.STATE_FILE)
        except ValueError:
            self.logger.debug("file %s is invalid." % self.STATE_FILE)
        return options


    def store_state(self, options):
        """Store options"""
        try:
            with open(self.STATE_FILE, 'w') as f:
                json.dump(options, f)
                self.logger.debug("Options saved.")
        except IOError:
            self.logger.debug("Cannot open %s." % self.STATE_FILE)


    def set_active_monitor(self, monitor):
        scr = self.get_screen()
        if monitor >= scr.get_n_monitors():
            self.monitor = 0
        else:
            self.monitor = monitor
        self.update_geometry()


    def on_monitors_changed(self, *_):
        self.set_active_monitor(self.monitor)


    def override_font_attributes(self, attr):
        window_width, window_height = self.get_size()
        attr.insert(pango.AttrSize((50 * window_height // 100) * 1000, 0, -1))
        attr.insert(pango.AttrFamily(self.font.get_family(), 0, -1))
        attr.insert(pango.AttrWeight(self.font.get_weight(), 0, -1))
        attr.insert(pango.AttrForeground(65535, 65535, 65535, 0, -1))


    def update_label(self):
        attr = self.label.get_attributes()
        self.override_font_attributes(attr)
        self.label.set_attributes(attr)


    def on_configure(self, *_):
        window_x, window_y = self.get_position()
        window_width, window_height = self.get_size()
        if self.options.position == 'fixed':
            # update internal geometry in order to handle user resizes
            self.options.geometry = [window_x, window_y, window_width, window_height]

        # set some proportional inner padding
        self.label.set_padding(window_width // 100, 0)

        self.update_label()


    def update_geometry(self, configure=False):
        if self.options.position == 'fixed' and self.options.geometry is not None:
            self.move(*self.options.geometry[0:2])
            self.resize(*self.options.geometry[2:4])
            return

        if self.options.geometry is not None:
            area_geometry = self.options.geometry
        else:
            geometry = self.get_screen().get_monitor_geometry(self.monitor)
            area_geometry = [geometry.x, geometry.y, geometry.width, geometry.height]

        if self.options.font_size == 'large':
            window_height = 24 * area_geometry[3] // 100
        elif self.options.font_size == 'medium':
            window_height = 12 * area_geometry[3] // 100
        else:
            window_height = 8 * area_geometry[3] // 100
        self.resize(area_geometry[2], window_height)

        if self.options.position == 'top':
            window_y = area_geometry[1] + window_height * 2
        elif self.options.position == 'center':
            window_y = area_geometry[1] + area_geometry[3] // 2
        else:
            window_y = area_geometry[1] + area_geometry[3] - window_height * 2
        self.move(area_geometry[0], window_y)


    def on_statusicon_popup(self, widget, button, timestamp, data=None):
        if button == 3 and data:
            data.show()
            data.popup(None, None, gtk.status_icon_position_menu,
                       3, timestamp, widget)


    def show(self):
        self.update_geometry()
        self.stick()
        super(Screenkey, self).show()


    def on_label_change(self, markup):
        attr, text, _ = pango.parse_markup(markup)
        self.override_font_attributes(attr)
        self.label.set_text(text)
        self.label.set_attributes(attr)

        if not self.get_property('visible'):
            self.show()
        if self.timer_hide:
            self.timer_hide.cancel()
        if self.options.timeout > 0:
            self.timer_hide = Timer(self.options.timeout, self.on_timeout_main)
            self.timer_hide.start()
        if self.timer_min:
            self.timer_min.cancel()
        self.timer_min = Timer(self.options.recent_thr * 2, self.on_timeout_min)
        self.timer_min.start()


    def on_timeout_main(self):
        if not self.options.persist:
            self.hide()
        self.label.set_text('')
        self.listenkbd.clear()


    def on_timeout_min(self):
        attr = self.label.get_attributes()
        attr.change(pango.AttrUnderline(pango.UNDERLINE_NONE, 0, -1))
        self.label.set_attributes(attr)


    def on_change_mode(self):
        if self.listenkbd:
            self.listenkbd.stop()
        self.listenkbd = ListenKbd(self.on_label_change, logger=self.logger,
                                   key_mode=self.options.key_mode,
                                   bak_mode=self.options.bak_mode,
                                   mods_mode=self.options.mods_mode,
                                   mods_only=self.options.mods_only,
                                   recent_thr=self.options.recent_thr)
        self.listenkbd.start()


    def on_show_keys(self, widget, data=None):
        if widget.get_active():
            self.logger.debug("Screenkey enabled.")
            self.listenkbd = ListenKbd(self.on_label_change, logger=self.logger,
                                       key_mode=self.options.key_mode,
                                       bak_mode=self.options.bak_mode,
                                       mods_mode=self.options.mods_mode,
                                       mods_only=self.options.mods_only,
                                       recent_thr=self.options.recent_thr)
            self.listenkbd.start()
        else:
            self.logger.debug("Screenkey disabled.")
            self.listenkbd.stop()


    def on_preferences_dialog(self, widget=None, data=None):
        self.prefs.show()


    def on_preferences_changed(self, widget=None, data=None):
        self.store_state(self.options)
        self.prefs.hide()


    def make_preferences_dialog(self):
        self.prefs = prefs = gtk.Dialog(APP_NAME, None,
                                        gtk.DIALOG_DESTROY_WITH_PARENT,
                                        (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
        prefs.connect("response", self.on_preferences_changed)

        def on_sb_time_changed(widget, data=None):
            self.options.timeout = widget.get_value()
            self.logger.debug("Timeout value changed: %f." % self.options.timeout)

        def on_cbox_sizes_changed(widget, data=None):
            index = widget.get_active()
            self.options.font_size = FONT_SIZES.keys()[index]
            self.update_geometry()
            self.logger.debug("Window size changed: %s." % self.options.font_size)

        def on_cbox_modes_changed(widget, data=None):
            index = widget.get_active()
            self.options.key_mode = KEY_MODES.keys()[index]
            self.on_change_mode()
            self.logger.debug("Key mode changed: %s." % self.options.key_mode)

        def on_cbox_bak_changed(widget, data=None):
            index = widget.get_active()
            self.options.bak_mode = BAK_MODES.keys()[index]
            self.on_change_mode()
            self.logger.debug("Bak mode changed: %s." % self.options.bak_mode)

        def on_cbox_mods_changed(widget, data=None):
            index = widget.get_active()
            self.options.mods_mode = MODS_MODES.keys()[index]
            self.on_change_mode()
            self.logger.debug("Mods mode changed: %s." % self.options.mods_mode)

        def on_cbox_modsonly_changed(widget, data=None):
            self.options.mods_only = widget.get_active()
            self.on_change_mode()
            self.logger.debug("Modifiers only changed: %s." % self.options.mods_only)

        def on_cbox_position_changed(widget, data=None):
            index = widget.get_active()
            self.options.position = POSITIONS.keys()[index]
            self.update_geometry()
            self.logger.debug("Window position changed: %s." % self.options.position)

        def on_cbox_screen_changed(widget, data=None):
            self.options.screen = widget.get_active()
            self.set_active_monitor(self.options.screen)
            self.logger.debug("Screen changed: %d." % self.options.screen)

        def on_cbox_persist_changed(widget, data=None):
            self.options.persist = widget.get_active()
            if not self.get_property('visible'):
                self.show()
            else:
                self.on_label_change(self.label.get_text())
            self.logger.debug("Screen changed: %d." % self.options.screen)

        def on_btn_forget(widget, data=None):
            self.options.geometry = None
            self.update_geometry()
            widget.hide()

        def on_btn_font(widget, data=None):
            self.options.font_desc = widget.get_font_name()
            self.font = pango.FontDescription(self.options.font_desc)
            self.update_label()

        frm_main = gtk.Frame(_("Preferences"))
        frm_main.set_border_width(6)
        vbox_main = gtk.VBox()

        frm_time = gtk.Frame("<b>%s</b>" % _("Time"))
        frm_time.set_border_width(4)
        frm_time.get_label_widget().set_use_markup(True)
        frm_time.set_shadow_type(gtk.SHADOW_NONE)
        vbox_time = gtk.VBox(spacing=6)
        hbox_time = gtk.HBox()
        lbl_time1 = gtk.Label(_("Display for"))
        lbl_time2 = gtk.Label(_("seconds"))
        sb_time = gtk.SpinButton(digits=1)
        sb_time.set_increments(0.5, 1.0)
        sb_time.set_range(0.5, 10.0)
        sb_time.set_numeric(True)
        sb_time.set_update_policy(gtk.UPDATE_IF_VALID)
        sb_time.set_value(self.options.timeout)
        sb_time.connect("value-changed", on_sb_time_changed)
        hbox_time.pack_start(lbl_time1, expand=False, fill=False, padding=6)
        hbox_time.pack_start(sb_time, expand=False, fill=False, padding=4)
        hbox_time.pack_start(lbl_time2, expand=False, fill=False, padding=4)
        vbox_time.pack_start(hbox_time)

        chk_persist = gtk.CheckButton(_("Persistent window"))
        chk_persist.connect("toggled", on_cbox_persist_changed)
        vbox_time.pack_start(chk_persist)

        frm_time.add(vbox_time)
        frm_time.show_all()

        frm_aspect = gtk.Frame("<b>%s</b>" % _("Aspect"))
        frm_aspect.set_border_width(4)
        frm_aspect.get_label_widget().set_use_markup(True)
        frm_aspect.set_shadow_type(gtk.SHADOW_NONE)
        vbox_aspect = gtk.VBox(spacing=6)

        hbox0_font = gtk.HBox()
        lbl_font = gtk.Label(_("Font"))
        btn_font = gtk.FontButton(self.options.font_desc)
        btn_font.set_use_size(False)
        btn_font.set_show_size(False)
        btn_font.connect("font-set", on_btn_font)
        hbox0_font.pack_start(lbl_font, expand=False, fill=False, padding=6)
        hbox0_font.pack_start(btn_font, expand=False, fill=False, padding=4)

        hbox0_aspect = gtk.HBox()

        lbl_screen = gtk.Label(_("Screen"))
        cbox_screen = gtk.combo_box_new_text()
        scr = self.get_screen()
        for n in range(scr.get_n_monitors()):
            cbox_screen.insert_text(n, '%d: %s' % (n, scr.get_monitor_plug_name(n)))
        cbox_screen.set_active(self.monitor)
        cbox_screen.connect("changed", on_cbox_screen_changed)

        hbox0_aspect.pack_start(lbl_screen, expand=False, fill=False, padding=6)
        hbox0_aspect.pack_start(cbox_screen, expand=False, fill=False, padding=4)

        hbox1_aspect = gtk.HBox()

        lbl_positions = gtk.Label(_("Position"))
        cbox_positions = gtk.combo_box_new_text()
        cbox_positions.set_name('position')
        for key, value in enumerate(POSITIONS):
            cbox_positions.insert_text(key, value)
        cbox_positions.set_active(POSITIONS.keys().index(self.options.position))
        cbox_positions.connect("changed", on_cbox_position_changed)

        hbox1_aspect.pack_start(lbl_positions, expand=False, fill=False, padding=6)
        hbox1_aspect.pack_start(cbox_positions, expand=False, fill=False, padding=4)

        hbox2_aspect = gtk.HBox()

        lbl_sizes = gtk.Label(_("Size"))
        cbox_sizes = gtk.combo_box_new_text()
        cbox_sizes.set_name('size')
        for key, value in enumerate(FONT_SIZES):
            cbox_sizes.insert_text(key, value)
        cbox_sizes.set_active(FONT_SIZES.keys().index(self.options.font_size))
        cbox_sizes.connect("changed", on_cbox_sizes_changed)

        hbox2_aspect.pack_start(lbl_sizes, expand=False, fill=False, padding=6)
        hbox2_aspect.pack_start(cbox_sizes, expand=False, fill=False, padding=4)

        vbox_aspect.pack_start(hbox0_font)
        vbox_aspect.pack_start(hbox0_aspect)
        vbox_aspect.pack_start(hbox1_aspect)
        vbox_aspect.pack_start(hbox2_aspect)

        if self.options.geometry:
            btn_forget = gtk.Button(_("Forget stored geometry"))
            btn_forget.connect("clicked", on_btn_forget)
            vbox_aspect.pack_start(btn_forget)

        frm_aspect.add(vbox_aspect)

        frm_kbd = gtk.Frame("<b>%s</b>" % _("Keys"))
        frm_kbd.set_border_width(4)
        frm_kbd.get_label_widget().set_use_markup(True)
        frm_kbd.set_shadow_type(gtk.SHADOW_NONE)
        vbox_kbd = gtk.VBox(spacing=6)

        hbox_kbd = gtk.HBox()
        lbl_kbd = gtk.Label(_("Insert mode"))
        cbox_modes = gtk.combo_box_new_text()
        cbox_modes.set_name('mode')
        for key, value in enumerate(KEY_MODES):
            cbox_modes.insert_text(key, value)
        cbox_modes.set_active(KEY_MODES.keys().index(self.options.key_mode))
        cbox_modes.connect("changed", on_cbox_modes_changed)
        hbox_kbd.pack_start(lbl_kbd, expand=False, fill=False, padding=6)
        hbox_kbd.pack_start(cbox_modes, expand=False, fill=False, padding=4)
        vbox_kbd.pack_start(hbox_kbd)

        hbox_kbd = gtk.HBox()
        lbl_kbd = gtk.Label(_("Backspace mode"))
        cbox_modes = gtk.combo_box_new_text()
        for key, value in enumerate(BAK_MODES):
            cbox_modes.insert_text(key, value)
        cbox_modes.set_active(BAK_MODES.keys().index(self.options.bak_mode))
        cbox_modes.connect("changed", on_cbox_bak_changed)
        hbox_kbd.pack_start(lbl_kbd, expand=False, fill=False, padding=6)
        hbox_kbd.pack_start(cbox_modes, expand=False, fill=False, padding=4)
        vbox_kbd.pack_start(hbox_kbd)

        hbox_kbd = gtk.HBox()
        lbl_kbd = gtk.Label(_("Modifiers mode"))
        cbox_modes = gtk.combo_box_new_text()
        for key, value in enumerate(MODS_MODES):
            cbox_modes.insert_text(key, value)
        cbox_modes.set_active(MODS_MODES.keys().index(self.options.mods_mode))
        cbox_modes.connect("changed", on_cbox_mods_changed)
        hbox_kbd.pack_start(lbl_kbd, expand=False, fill=False, padding=6)
        hbox_kbd.pack_start(cbox_modes, expand=False, fill=False, padding=4)
        vbox_kbd.pack_start(hbox_kbd)

        chk_kbd = gtk.CheckButton(_("Modifiers only"))
        chk_kbd.connect("toggled", on_cbox_modsonly_changed)
        vbox_kbd.pack_start(chk_kbd)

        frm_kbd.add(vbox_kbd)

        vbox_main.pack_start(frm_time, False, False, 6)
        vbox_main.pack_start(frm_aspect, False, False, 6)
        vbox_main.pack_start(frm_kbd, False, False, 6)
        frm_main.add(vbox_main)

        prefs.vbox.pack_start(frm_main)
        prefs.set_destroy_with_parent(True)
        prefs.set_resizable(False)
        prefs.set_has_separator(False)
        prefs.set_default_response(gtk.RESPONSE_CLOSE)
        prefs.vbox.show_all()


    def make_menu(self):
        self.menu = menu = gtk.Menu()

        show_item = gtk.CheckMenuItem(_("Show keys"))
        show_item.set_active(True)
        show_item.connect("toggled", self.on_show_keys)
        show_item.show()
        menu.append(show_item)

        preferences_item = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
        preferences_item.connect("activate", self.on_preferences_dialog)
        preferences_item.show()
        menu.append(preferences_item)

        about_item = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        about_item.connect("activate", self.on_about_dialog)
        about_item.show()
        menu.append(about_item)

        separator_item = gtk.SeparatorMenuItem()
        separator_item.show()
        menu.append(separator_item)

        image = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        image.connect("activate", self.quit)
        image.show()
        menu.append(image)
        menu.show()


    def make_systray(self):
        try:
            import appindicator
            self.systray = appindicator.Indicator(
                APP_NAME, 'indicator-messages', appindicator.CATEGORY_APPLICATION_STATUS)
            self.systray.set_status(appindicator.STATUS_ACTIVE)
            self.systray.set_attention_icon("indicator-messages-new")
            self.systray.set_icon("preferences-desktop-keyboard-shortcuts")
            self.systray.set_menu(self.menu)
            self.logger.debug("Using AppIndicator.")
        except ImportError:
            self.systray = gtk.StatusIcon()
            self.systray.set_from_icon_name("preferences-desktop-keyboard-shortcuts")
            self.systray.connect("popup-menu", self.on_statusicon_popup, self.menu)
            self.logger.debug("Using StatusIcon.")


    def make_about_dialog(self):
        self.about = about = gtk.AboutDialog()
        about.set_program_name(APP_NAME)
        about.set_version(VERSION)
        about.set_copyright("""
        Copyright(c) 2010-2012 Pablo Seminario <pabluk@gmail.com>
        Copyright(c) 2015 by wave++ "Yuri D'Elia" <wavexx@thregr.org>
        """)

        about.set_comments(APP_DESC)
        about.set_documenters(
                ["José María Quiroga <pepelandia@gmail.com>"]
        )
        about.set_website(APP_URL)
        about.set_icon_name('preferences-desktop-keyboard-shortcuts')
        about.set_logo_icon_name('preferences-desktop-keyboard-shortcuts')
        about.connect("response", lambda *_: about.hide())


    def on_about_dialog(self, widget, data=None):
        self.about.show()



def run():
    glib.threads_init()
    gtk.main()
