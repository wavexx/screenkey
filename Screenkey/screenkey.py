# -*- coding: utf-8 -*-
# "screenkey" is distributed under GNU GPLv3+, WITHOUT ANY WARRANTY.
# Copyright(c) 2010-2012: Pablo Seminario <pabluk@gmail.com>
# Copyright(c) 2015-2016: wave++ "Yuri D'Elia" <wavexx@thregr.org>.

from __future__ import print_function, unicode_literals, division

from . import *
from .labelmanager import LabelManager

from threading import Timer
import json
import os
import subprocess

import glib
glib.threads_init()

import pygtk
pygtk.require('2.0')

import gtk
import pango


class Screenkey(gtk.Window):
    STATE_FILE = os.path.join(glib.get_user_config_dir(), 'screenkey.json')

    def __init__(self, logger, options, show_settings=False):
        gtk.Window.__init__(self, gtk.WINDOW_POPUP)

        self.timer_hide = None
        self.timer_min = None
        self.logger = logger

        defaults = Options({'no_systray': False,
                            'timeout': 2.5,
                            'recent_thr': 0.1,
                            'compr_cnt': 3,
                            'ignore': [],
                            'position': 'bottom',
                            'persist': False,
                            'font_desc': 'Sans Bold',
                            'font_size': 'medium',
                            'font_color': 'white',
                            'bg_color': 'black',
                            'opacity': 0.8,
                            'key_mode': 'composed',
                            'bak_mode': 'baked',
                            'mods_mode': 'normal',
                            'mods_only': False,
                            'multiline': False,
                            'vis_shift': False,
                            'vis_space': True,
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

        self.set_keep_above(True)
        self.set_accept_focus(False)
        self.set_focus_on_map(False)

        self.label = gtk.Label()
        self.label.set_attributes(pango.AttrList())
        self.label.set_ellipsize(pango.ELLIPSIZE_START)
        self.label.set_justify(gtk.JUSTIFY_CENTER)
        self.label.show()
        self.add(self.label)

        self.set_gravity(gtk.gdk.GRAVITY_CENTER)
        self.connect("configure-event", self.on_configure)
        scr = self.get_screen()
        scr.connect("size-changed", self.on_configure)
        scr.connect("monitors-changed", self.on_monitors_changed)
        self.set_active_monitor(self.options.screen)

        self.font = pango.FontDescription(self.options.font_desc)
        self.update_colors()
        self.update_label()

        self.labelmngr = None
        self.enabled = True
        self.on_change_mode()

        self.make_menu()
        self.make_about_dialog()
        self.make_preferences_dialog()

        if not self.options.no_systray:
            self.make_systray()

        self.connect("delete-event", self.quit)
        if show_settings:
            self.on_preferences_dialog()
        if self.options.persist:
            self.show()


    def quit(self, widget, data=None):
        self.labelmngr.stop()
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

        # compatibility with previous versions (0.5)
        if options and options.key_mode == 'normal':
            options.key_mode = 'composed'

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


    def override_font_attributes(self, attr, text):
        window_width, window_height = self.get_size()
        lines = text.count('\n') + 1
        attr.insert(pango.AttrSizeAbsolute((50 * window_height // lines // 100) * 1000, 0, -1))
        attr.insert(pango.AttrFamily(self.font.get_family(), 0, -1))
        attr.insert(pango.AttrWeight(self.font.get_weight(), 0, -1))


    def update_label(self):
        attr = self.label.get_attributes()
        text = self.label.get_text()
        self.override_font_attributes(attr, text)
        self.label.set_attributes(attr)


    def update_colors(self):
        self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.options.font_color))
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.options.bg_color))
        self.set_opacity(self.options.opacity)


    def on_configure(self, *_):
        window_x, window_y = self.get_position()
        window_width, window_height = self.get_size()

        mask = gtk.gdk.Pixmap(None, window_width, window_height, 1)
        gc = gtk.gdk.GC(mask)
        gc.set_foreground(gtk.gdk.Color(pixel=0))
        mask.draw_rectangle(gc, True, 0, 0, window_width, window_height)
        self.input_shape_combine_mask(mask, 0, 0)

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
        super(Screenkey, self).show()


    def on_label_change(self, markup):
        attr, text, _ = pango.parse_markup(markup)
        self.override_font_attributes(attr, text)
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
        self.labelmngr.clear()


    def on_timeout_min(self):
        attr = self.label.get_attributes()
        attr.change(pango.AttrUnderline(pango.UNDERLINE_NONE, 0, -1))
        self.label.set_attributes(attr)


    def restart_labelmanager(self):
        self.logger.debug("Restarting LabelManager.")
        if self.labelmngr:
            self.labelmngr.stop()
        self.labelmngr = LabelManager(self.on_label_change, logger=self.logger,
                                      key_mode=self.options.key_mode,
                                      bak_mode=self.options.bak_mode,
                                      mods_mode=self.options.mods_mode,
                                      mods_only=self.options.mods_only,
                                      multiline=self.options.multiline,
                                      vis_shift=self.options.vis_shift,
                                      vis_space=self.options.vis_space,
                                      recent_thr=self.options.recent_thr,
                                      compr_cnt=self.options.compr_cnt,
                                      ignore=self.options.ignore,
                                      pango_ctx=self.label.get_pango_context())
        self.labelmngr.start()


    def on_change_mode(self):
        if not self.enabled:
            return
        self.restart_labelmanager()


    def on_show_keys(self, widget, data=None):
        self.enabled = widget.get_active()
        if self.enabled:
            self.logger.debug("Screenkey enabled.")
            self.restart_labelmanager()
        else:
            self.logger.debug("Screenkey disabled.")
            self.labelmngr.stop()


    def on_preferences_dialog(self, widget=None, data=None):
        self.prefs.show()


    def on_preferences_changed(self, widget=None, data=None):
        self.store_state(self.options)
        self.prefs.hide()
        return True


    def make_preferences_dialog(self):
        # TODO: switch to something declarative or at least clean-up the following mess
        self.prefs = prefs = gtk.Dialog(APP_NAME, None,
                                        gtk.DIALOG_DESTROY_WITH_PARENT,
                                        (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
        prefs.connect("response", self.on_preferences_changed)
        prefs.connect("delete-event", self.on_preferences_changed)

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

        def on_cbox_visshift_changed(widget, data=None):
            self.options.vis_shift = widget.get_active()
            self.on_change_mode()
            self.logger.debug("Visible Shift changed: %s." % self.options.vis_shift)

        def on_cbox_visspace_changed(widget, data=None):
            self.options.vis_space = widget.get_active()
            self.on_change_mode()
            self.logger.debug("Show Whitespace changed: %s." % self.options.vis_space)

        def on_cbox_position_changed(widget, data=None):
            index = widget.get_active()
            new_position = POSITIONS.keys()[index]
            if new_position == 'fixed':
                new_geom = on_btn_sel_geom(widget)
                if not new_geom:
                    self.cbox_positions.set_active(POSITIONS.keys().index(self.options.position))
                    return
            elif self.options.position == 'fixed':
                # automatically clear geometry
                self.options.geometry = None
            self.options.position = new_position
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
            self.logger.debug("Persistent changed: %s." % self.options.persist)

        def on_sb_compr_changed(widget, data=None):
            self.options.compr_cnt = widget.get_value_as_int()
            self.on_change_mode()
            self.logger.debug("Compress repeats value changed: %d." % self.options.compr_cnt)

        def on_cbox_compr_changed(widget, data=None):
            compr_enabled = widget.get_active()
            self.sb_compr.set_sensitive(compr_enabled)
            self.options.compr_cnt = self.sb_compr.get_value_as_int() if compr_enabled else 0
            self.on_change_mode()
            self.logger.debug("Compress repeats value changed: %d." % self.options.compr_cnt)

        def on_btn_sel_geom(widget, data=None):
            try:
                ret = subprocess.check_output(['slop', '-f', '%x %y %w %h'])
            except subprocess.CalledProcessError:
                return False
            except OSError:
                msg = gtk.MessageDialog(parent=self,
                                        type=gtk.MESSAGE_ERROR,
                                        buttons=gtk.BUTTONS_OK,
                                        message_format="Error running \"slop\"")
                msg.format_secondary_markup("\"slop\" is required for interactive selection. "
                                            "See <a href=\"https://github.com/naelstrof/slop\">"
                                            "https://github.com/naelstrof/slop</a>")
                msg.run()
                msg.destroy()
                return False

            self.options.geometry = map(int, ret.split(' '))
            self.update_geometry()
            self.btn_reset_geom.set_sensitive(True)
            return True

        def on_btn_reset_geom(widget, data=None):
            self.options.geometry = None
            if self.options.position == 'fixed':
                self.options.position = 'bottom'
                self.cbox_positions.set_active(POSITIONS.keys().index(self.options.position))
            self.update_geometry()
            widget.set_sensitive(False)

        def on_adj_opacity_changed(widget, data=None):
            self.options.opacity = widget.get_value()
            self.update_colors()

        def on_font_color_changed(widget, data=None):
            self.options.font_color = widget.get_color().to_string()
            self.update_colors()

        def on_bg_color_changed(widget, data=None):
            self.options.bg_color = widget.get_color().to_string()
            self.update_colors()

        def on_btn_font(widget, data=None):
            self.options.font_desc = widget.get_font_name()
            self.font = pango.FontDescription(self.options.font_desc)
            self.update_label()

        frm_main = gtk.Frame(_("Preferences"))
        frm_main.set_border_width(6)

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
        chk_persist.set_active(self.options.persist)
        vbox_time.pack_start(chk_persist)

        frm_time.add(vbox_time)
        frm_time.show_all()

        frm_position = gtk.Frame("<b>%s</b>" % _("Position"))
        frm_position.set_border_width(4)
        frm_position.get_label_widget().set_use_markup(True)
        frm_position.set_shadow_type(gtk.SHADOW_NONE)
        vbox_position = gtk.VBox(spacing=6)

        lbl_screen = gtk.Label(_("Screen"))
        cbox_screen = gtk.combo_box_new_text()
        scr = self.get_screen()
        for n in range(scr.get_n_monitors()):
            cbox_screen.insert_text(n, '%d: %s' % (n, scr.get_monitor_plug_name(n)))
        cbox_screen.set_active(self.monitor)
        cbox_screen.connect("changed", on_cbox_screen_changed)

        hbox0_position = gtk.HBox()
        hbox0_position.pack_start(lbl_screen, expand=False, fill=False, padding=6)
        hbox0_position.pack_start(cbox_screen, expand=False, fill=False, padding=4)
        vbox_position.pack_start(hbox0_position)

        lbl_positions = gtk.Label(_("Position"))
        self.cbox_positions = cbox_positions = gtk.combo_box_new_text()
        cbox_positions.set_name('position')
        for key, value in enumerate(POSITIONS):
            cbox_positions.insert_text(key, value)
        cbox_positions.set_active(POSITIONS.keys().index(self.options.position))
        cbox_positions.connect("changed", on_cbox_position_changed)

        self.btn_reset_geom = btn_reset_geom = gtk.Button(_("Reset"))
        btn_reset_geom.connect("clicked", on_btn_reset_geom)
        btn_reset_geom.set_sensitive(self.options.geometry is not None)

        hbox1_position = gtk.HBox()
        hbox1_position.pack_start(lbl_positions, expand=False, fill=False, padding=6)
        hbox1_position.pack_start(cbox_positions, expand=False, fill=False, padding=4)
        hbox1_position.pack_start(btn_reset_geom, expand=False, fill=False, padding=4)
        vbox_position.pack_start(hbox1_position)

        btn_sel_geom = gtk.Button(_("Select window/region"))
        btn_sel_geom.connect("clicked", on_btn_sel_geom)
        vbox_position.pack_start(btn_sel_geom)

        frm_aspect = gtk.Frame("<b>%s</b>" % _("Aspect"))
        frm_aspect.set_border_width(4)
        frm_aspect.get_label_widget().set_use_markup(True)
        frm_aspect.set_shadow_type(gtk.SHADOW_NONE)
        vbox_aspect = gtk.VBox(spacing=6)

        frm_position.add(vbox_position)

        hbox0_font = gtk.HBox()
        lbl_font = gtk.Label(_("Font"))
        btn_font = gtk.FontButton(self.options.font_desc)
        btn_font.set_use_size(False)
        btn_font.set_show_size(False)
        btn_font.connect("font-set", on_btn_font)
        hbox0_font.pack_start(lbl_font, expand=False, fill=False, padding=6)
        hbox0_font.pack_start(btn_font, expand=False, fill=False, padding=4)

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

        hbox3_font_color = gtk.HBox()

        lbl_font_color = gtk.Label(_("Font color"))
        btn_font_color = gtk.ColorButton(color=gtk.gdk.color_parse(self.options.font_color))
        btn_font_color.connect("color-set", on_font_color_changed)
        btn_bg_color = gtk.ColorButton(color=gtk.gdk.color_parse(self.options.bg_color))
        btn_bg_color.connect("color-set", on_bg_color_changed)

        hbox3_font_color.pack_start(lbl_font_color, expand=False, fill=False, padding=6)
        hbox3_font_color.pack_start(btn_font_color, expand=False, fill=False, padding=4)
        hbox3_font_color.pack_start(btn_bg_color, expand=False, fill=False, padding=4)

        hbox4_aspect = gtk.HBox()

        lbl_opacity = gtk.Label(_("Opacity"))
        adj_opacity = gtk.Adjustment(self.options.opacity, 0.1, 1.0, 0.1, 0, 0)
        adj_opacity.connect("value-changed", on_adj_opacity_changed)
        adj_scale = gtk.HScale(adj_opacity)

        hbox4_aspect.pack_start(lbl_opacity, expand=False, fill=False, padding=6)
        hbox4_aspect.pack_start(adj_scale, expand=True, fill=True, padding=4)

        vbox_aspect.pack_start(hbox0_font)
        vbox_aspect.pack_start(hbox2_aspect)
        vbox_aspect.pack_start(hbox3_font_color)
        vbox_aspect.pack_start(hbox4_aspect)

        frm_aspect.add(vbox_aspect)

        frm_kbd = gtk.Frame("<b>%s</b>" % _("Keys"))
        frm_kbd.set_border_width(4)
        frm_kbd.get_label_widget().set_use_markup(True)
        frm_kbd.set_shadow_type(gtk.SHADOW_NONE)
        vbox_kbd = gtk.VBox(spacing=6)

        hbox_kbd = gtk.HBox()
        lbl_kbd = gtk.Label(_("Keyboard mode"))
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

        chk_kbd = gtk.CheckButton(_("Show Modifier sequences only"))
        chk_kbd.connect("toggled", on_cbox_modsonly_changed)
        chk_kbd.set_active(self.options.mods_only)
        vbox_kbd.pack_start(chk_kbd)

        chk_kbd = gtk.CheckButton(_("Always show Shift"))
        chk_kbd.connect("toggled", on_cbox_visshift_changed)
        chk_kbd.set_active(self.options.vis_shift)
        vbox_kbd.pack_start(chk_kbd)

        chk_vspace = gtk.CheckButton(_("Show Whitespace characters"))
        chk_vspace.connect("toggled", on_cbox_visspace_changed)
        chk_vspace.set_active(self.options.vis_space)
        vbox_kbd.pack_start(chk_vspace)

        hbox_compr = gtk.HBox()
        chk_compr = gtk.CheckButton(_("Compress repeats after"))
        chk_compr.set_active(self.options.compr_cnt > 0)
        chk_compr.connect("toggled", on_cbox_compr_changed)
        self.sb_compr = sb_compr = gtk.SpinButton(digits=0)
        sb_compr.set_increments(1, 1)
        sb_compr.set_range(1, 100)
        sb_compr.set_numeric(True)
        sb_compr.set_update_policy(gtk.UPDATE_IF_VALID)
        sb_compr.set_value(self.options.compr_cnt or 3)
        sb_compr.connect("value-changed", on_sb_compr_changed)
        hbox_compr.pack_start(chk_compr, expand=False, fill=False)
        hbox_compr.pack_start(sb_compr, expand=False, fill=False, padding=4)
        vbox_kbd.pack_start(hbox_compr)

        frm_kbd.add(vbox_kbd)

        hbox_main = gtk.HBox()
        vbox_main = gtk.VBox()
        vbox_main.pack_start(frm_time, False, False, 6)
        vbox_main.pack_start(frm_position, False, False, 6)
        vbox_main.pack_start(frm_aspect, False, False, 6)
        hbox_main.pack_start(vbox_main)
        vbox_main = gtk.VBox()
        vbox_main.pack_start(frm_kbd, False, False, 6)
        hbox_main.pack_start(vbox_main)
        frm_main.add(hbox_main)

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
        Copyright(c) 2010-2012: Pablo Seminario <pabluk@gmail.com>
        Copyright(c) 2015-2016: wave++ "Yuri D'Elia" <wavexx@thregr.org>
        """)
        about.set_comments(APP_DESC)
        about.set_documenters(
                ["José María Quiroga <pepelandia@gmail.com>"]
        )
        about.set_website(APP_URL)
        about.set_icon_name('preferences-desktop-keyboard-shortcuts')
        about.set_logo_icon_name('preferences-desktop-keyboard-shortcuts')
        about.connect("response", about.hide_on_delete)
        about.connect("delete-event", about.hide_on_delete)


    def on_about_dialog(self, widget, data=None):
        self.about.show()



def run():
    gtk.main()
