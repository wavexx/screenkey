#!/usr/bin/env python
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

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import pango
from threading import Timer
from listenkdb import ListenKbd

gtk.gdk.threads_init()

APP_NAME = 'Screenkey'
APP_DESC = 'Screencast your keys'
APP_URL = 'http://launchpad.net/screenkey'
VERSION = '0.1'
AUTHOR = 'Pablo Seminario'

class Screenkey(gtk.Window):

    def __init__(self):
        gtk.Window.__init__(self)

        self.timer = None

        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_keep_above(True)
        self.set_decorated(False)
        self.stick()
        self.set_property('accept-focus', False)
        self.set_property('focus-on-map', False)
        self.set_position(gtk.WIN_POS_CENTER)
        bgcolor = gtk.gdk.color_parse("black")
        self.modify_bg(gtk.STATE_NORMAL, bgcolor)
        self.set_opacity(0.7)

        self.set_gravity(gtk.gdk.GRAVITY_CENTER)

        self.screen_width = gtk.gdk.screen_width()   
        self.screen_height = gtk.gdk.screen_height() 
        window_width = self.screen_width
        window_height = 12 * self.screen_height / 100
        self.set_default_size(window_width, window_height)
        self.move(0, self.screen_height - window_height * 2)

        gobject.signal_new("text-changed", gtk.Label, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
        attr = pango.AttrList()
        attr.change(pango.AttrSize((50 * window_height / 100) * 1000, 0, -1))
        attr.change(pango.AttrFamily("Sans", 0, -1))
        attr.change(pango.AttrWeight(pango.WEIGHT_BOLD, 0, -1))
        attr.change(pango.AttrForeground(65535, 65535, 65535, 0, -1))
        self.label = gtk.Label()
        self.label.set_attributes(attr)
        self.label.set_justify(gtk.JUSTIFY_RIGHT)
        self.label.set_ellipsize(pango.ELLIPSIZE_START)
        self.label.connect("text-changed", self.on_label_change)
        self.label.show()
        self.add(self.label)

        self.listenkbd = ListenKbd(self.label)
        self.listenkbd.start()


        menu = gtk.Menu()

        show_item = gtk.CheckMenuItem("Show keys")
        show_item.set_active(True)
        show_item.connect("toggled", self.on_show_keys)
        show_item.show()
        menu.append(show_item)

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

        try:
            import appindicator
            self.systray = appindicator.Indicator(APP_NAME, 'indicator-messages', appindicator.CATEGORY_APPLICATION_STATUS)
            self.systray.set_status (appindicator.STATUS_ACTIVE)
            self.systray.set_attention_icon ("indicator-messages-new")
            self.systray.set_icon("preferences-desktop-keyboard-shortcuts")
            self.systray.set_menu(menu)
        except(ImportError):
            self.systray = gtk.StatusIcon()
            self.systray.set_from_stock(gtk.STOCK_ITALIC)
            self.systray.connect("popup-menu", self.on_statusicon_popup, menu)


        self.connect("delete-event", self.quit)

    def quit(self, widget, data=None):
        self.listenkbd.stop()
        gtk.main_quit()

    def on_statusicon_popup(self, widget, button, timestamp, data=None):
        if button == 3:
            if data:
                data.show()
                data.popup(None, None, gtk.status_icon_position_menu, 3, timestamp, widget)

    def on_label_change(self, widget, data=None):
        if not self.get_property('visible'):
            gtk.gdk.threads_enter()
            window_width, window_height = self.get_size()
            self.move(0, self.screen_height - window_height * 2)
            self.stick()
            self.show()
            gtk.gdk.threads_leave()
        if self.timer:
            self.timer.cancel()

        self.timer = Timer(2.5, self.on_timeout)
        self.timer.start()

    def on_timeout(self):
        self.hide()
        self.label.set_text("")

    def on_show_keys(self, widget, data=None):
        if widget.get_active():
            self.listenkbd.stopEvent.clear()
            self.listenkbd = ListenKbd(self.label)
            self.listenkbd.start()
        else:
            self.listenkbd.stop()

    def on_about_dialog(self, widget, data=None):
        about = gtk.AboutDialog()
        about.set_program_name(APP_NAME)
        about.set_version(VERSION)
        about.set_copyright(u"2010 \u00a9 %s" % AUTHOR)
        about.set_comments(APP_DESC)
        about.set_documenters(["Jose Maria Quiroga <pepelandia@gmail.com>"])
        about.set_website(APP_URL)
        about.set_icon_name('preferences-desktop-keyboard-shortcuts')
        about.set_logo_icon_name('preferences-desktop-keyboard-shortcuts')
        about.run()
        about.destroy()


def Main():
    s = Screenkey()
    gtk.main()


if __name__ == "__main__":
    Main()

