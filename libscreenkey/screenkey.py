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
        window_height = 10 * self.screen_height / 100
        self.set_default_size(window_width, window_height)
        self.move(0, self.screen_height - window_height * 2)

        gobject.signal_new("text-changed", gtk.Label, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
        self.label = gtk.Label("screenkey")
        self.label.set_use_markup(True)
        self.label.set_justify(gtk.JUSTIFY_RIGHT)
        self.label.set_ellipsize(pango.ELLIPSIZE_START)
        self.label.connect("text-changed", self.on_label_change)
        self.label.show()
        self.add(self.label)

        self.listenkbd = ListenKbd(self.label)
        self.listenkbd.start()

        try:
            import appindicator
            self.systray = appindicator.Indicator(APP_NAME, 'indicator-messages', appindicator.CATEGORY_APPLICATION_STATUS)
            self.systray.set_status (appindicator.STATUS_ACTIVE)
            self.systray.set_attention_icon ("indicator-messages-new")
            self.systray.set_icon("gtk-bold")
        except(ImportError):
            self.systray = gtk.StatusIcon()
            self.systray.set_from_stock(gtk.STOCK_ITALIC)


        menu = gtk.Menu()

        check = gtk.CheckMenuItem("Run thread")
        check.set_active(True)
        check.connect("toggled", self.on_thread_toggle)
        check.show()
        menu.append(check)

        show_item = gtk.CheckMenuItem("Show window")
        show_item.set_active(True)
        show_item.connect("toggled", self.on_window_show_toggle)
        show_item.show()
        menu.append(show_item)

        image = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        image.connect("activate", self.quit)
        image.show()
        menu.append(image)
                    
        menu.show()

        self.systray.set_menu(menu)

        

        self.connect("delete-event", self.quit)
        #self.show_all()

    def quit(self, widget, data=None):
        self.listenkbd.stop()
        gtk.main_quit()

    def on_label_change(self, widget, data=None):
        if not self.get_property('visible'):
            gtk.gdk.threads_enter()
            window_width, window_height = self.get_size()
            self.move(0, self.screen_height - window_height * 2)
            self.show()
            gtk.gdk.threads_leave()
        if self.timer:
            self.timer.cancel()

        self.timer = Timer(2.5, self.hide)
        self.timer.start()

    def on_window_show_toggle(self, widget, data=None):
        if widget.get_active():
            self.show()
        else:
            self.hide()

    def on_thread_toggle(self, widget, data=None):
        if widget.get_active():
            self.listenkbd.stopEvent.clear()
            self.listenkbd = ListenKbd(self.label)
            self.listenkbd.start()
        else:
            self.listenkbd.stop()

def Main():
    s = Screenkey()
    gtk.main()


if __name__ == "__main__":
    Main()

