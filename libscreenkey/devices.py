#!/usr/bin/env python

"""
    Keyboard / Mouse Autodiscovery
    ==============================
    A set of tools to discover various input devices through HAL. This code has
    been adapted from the Arista Transcoder project. It will dynamically find
    keyboard and mouse input device nodes as they are created or destroyed from
    users plugging or unplugging them.
    
    See the bottom of the file for an example of how to use this code.
    
    License
    -------
    Copyright 2008 - 2009 Daniel G. Taylor <dan@programmer-art.org>

    Permission is hereby granted, free of charge, to any person obtaining a 
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
"""

import gettext

import gobject
import dbus

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

class InputSource(object):
    """
        A simple object representing an input source.
    """
    def __init__(self, udi, interface):
        """
            Create a new input device.
            
            @type udi: string
            @param udi: The HAL device identifier for this device.
            @type interface: dbus.Interface
            @param interface: The Hal.Device DBus interface for this device.
        """
        self.udi = udi
        self.interface = interface
        self.product = interface.GetProperty("info.product")
        self.block = interface.GetProperty("input.device")

class InputFinder(gobject.GObject):
    """
        An object that will find and monitor input sources (keyboards, mice) 
        and emit signals when such devices are added or removed from the
        system.
        
        Signals:
        
         - keyboard-found(InputFinder, InputSource)
         - keyboard-lost(InputFinder, InputSource)
         - mouse-found(InputFinder, InputSource)
         - mouse-lost(InputFinder, InputSource)
        
        Note that initially plugged-in devices will not throw a signal,
        instead you must iterate over them yourself if you wish to discover
        them.
        
            >>> devices = InputFinder()
            >>> print devices.keyboards
            >>> print devices.mice
        
    """
    
    __gsignals__ = {
        "keyboard-found": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
                           (gobject.TYPE_PYOBJECT,)),
        "keyboard-lost": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
                          (gobject.TYPE_PYOBJECT,)),
        "mouse-found": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                        (gobject.TYPE_PYOBJECT,)),
        "mouse-lost": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                       (gobject.TYPE_PYOBJECT,)),
    }
    
    def __init__(self):
        """
            Create a new InputFinder and attach to the DBus system bus to find
            device information through HAL.
        """
        self.__gobject_init__()
        self.bus = dbus.SystemBus()
        self.hal_obj = self.bus.get_object("org.freedesktop.Hal",
                                           "/org/freedesktop/Hal/Manager")
        self.hal = dbus.Interface(self.hal_obj, "org.freedesktop.Hal.Manager")
        
        self.keyboards = {}
        self.mice = {}
        
        udis = self.hal.FindDeviceByCapability("input.keyboard")
        for udi in udis:
            dev_obj = self.bus.get_object("org.freedesktop.Hal", udi)
            dev = dbus.Interface(dev_obj, "org.freedesktop.Hal.Device")
            block = dev.GetProperty("input.device")
            self.keyboards[block] = InputSource(udi, dev)
        
        udis = self.hal.FindDeviceByCapability("input.mouse")
        for udi in udis:
            dev_obj = self.bus.get_object("org.freedesktop.Hal", udi)
            dev = dbus.Interface(dev_obj, "org.freedesktop.Hal.Device")
            block = dev.GetProperty("input.device")
            self.mice[block] = InputSource(udi, dev)
        
        self.hal.connect_to_signal("DeviceAdded", self.device_added)
        self.hal.connect_to_signal("DeviceRemoved", self.device_removed)
    
    def device_added(self, udi):
        """
            Called when a device has been added to the system. If the device
            is a keyboard or a mouse, a signal will be emitted.
        """
        dev_obj = self.bus.get_object("org.freedesktop.Hal", udi)
        dev = dbus.Interface(dev_obj, "org.freedesktop.Hal.Device")
        if dev.PropertyExists("input.device"):
            block = dev.GetProperty("input.device")
            if dev.QueryCapability("input.keyboard"):
                self.keyboards[block] = InputSource(udi, dev)
                self.emit("keyboard-found", self.keyboards[block])
            elif dev.QueryCapability("input.mouse"):
                self.mice[block] = InputSource(udi, dev)
                self.emit("mouse-found", self.mice[block])
    
    def device_removed(self, udi):
        """
            Called when a device has been removed from the signal. If the
            device is a keyboard or a mouse, a signal will be emitted.
        """
        for block, keyboard in self.keyboards.items():
            if keyboard.udi == udi:
                self.emit("keyboard-lost", keyboard)
                del self.keyboards[block]
                break
        
        for block, mouse in self.mice.items():
            if mouse.udi == udi:
                self.emit("mouse-lost", mouse)
                del self.mice[block]
                break


gobject.type_register(InputFinder)

if __name__ == "__main__":
    # Run a test to print out input devices
    import gobject
    gobject.threads_init()
    
    def found(finder, device):
        print "Found %(name)s (%(block)s)" % {
            "name": device.product,
            "block": device.block,
        }
    
    def lost(finder, device):
        print "Lost %(name)s (%(block)s)" % {
            "name": device.product,
            "block": device.block,
        }
    
    finder = InputFinder()
    finder.connect("keyboard-found", found)
    finder.connect("keyboard-lost", lost)
    finder.connect("mouse-found", found)
    finder.connect("mouse-lost", lost)
    
    print "Currently plugged in:"
    
    for block, keyboard in finder.keyboards.items():
        print "Keyboard: %(name)s (%(block)s)" % {
            "name": keyboard.product,
            "block": keyboard.block,
        }
    
    for block, mouse in finder.mice.items():
        print "Mouse: %(name)s (%(block)s)" % {
            "name": mouse.product,
            "block": mouse.block,
        }
    
    print "Watching for new devices..."
    
    loop = gobject.MainLoop()
    loop.run()

