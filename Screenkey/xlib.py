# -*- coding: utf-8 -*-
# Distributed under the GNU GPLv3+ license, WITHOUT ANY WARRANTY.
# Copyright(c) 2015: wave++ "Yuri D'Elia" <wavexx@thregr.org>

from __future__ import unicode_literals
from ctypes import *

## base X11
libX11 = CDLL('libX11.so.6')

# types
Atom = c_ulong
Bool = c_int
XID = c_ulong
Colormap = XID
Cursor = XID
KeyCode = c_ubyte
KeySym = XID
Pixmap = XID
Status = c_int
String = c_char_p
Time = c_ulong
Window = XID

class Display(Structure):
    pass

class Visual(Structure):
    pass

class XKeyEvent(Structure):
    _fields_ = [('type', c_int),
                ('serial', c_ulong),
                ('send_event', Bool),
                ('display', POINTER(Display)),
                ('window', Window),
                ('root', Window),
                ('subwindow', Window),
                ('time', Time),
                ('x', c_int),
                ('y', c_int),
                ('x_root', c_int),
                ('y_root', c_int),
                ('state', c_uint),
                ('keycode', c_uint),
                ('same_screen', Bool)]

XKeyPressedEvent = XKeyEvent
XKeyReleasedEvent = XKeyEvent

class XClientMessageEvent(Structure):
    _fields_ = [('type', c_int),
                ('serial', c_ulong),
                ('send_event', Bool),
                ('display', POINTER(Display)),
                ('window', Window),
                ('message_type', Atom),
                ('format', c_int),
                ('data', c_long * 5)]

class XEvent(Union):
    _fields_ = [('type', c_int),
                ('xkey', XKeyEvent),
                ('xclient', XClientMessageEvent),
                ('pad', c_long * 24)]

class XSetWindowAttributes(Structure):
    _fields_ = [('background_pixmap', Pixmap),
                ('background_pixel', c_ulong),
                ('border_pixmap', Pixmap),
                ('border_pixel', c_ulong),
                ('bit_gravity', c_int),
                ('win_gravity', c_int),
                ('backing_store', c_int),
                ('backing_planes', c_ulong),
                ('backing_pixel', c_ulong),
                ('save_under', Bool),
                ('event_mask', c_long),
                ('do_not_propagate_mask', c_long),
                ('override_redirect', Bool),
                ('colormap', Colormap),
                ('cursor', Cursor)]


# constants
KeyPress = 2
KeyRelease = 3
FocusIn = 9
FocusOut = 10
ClientMessage = 33

CopyFromParent = 0
InputOnly = 2

CWOverrideRedirect = (1<<9)

ShiftMask = (1<<0)
LockMask = (1<<1)
ControlMask = (1<<2)
Mod1Mask = (1<<3)
Mod2Mask = (1<<4)
Mod3Mask = (1<<5)
Mod4Mask = (1<<6)
Mod5Mask = (1<<7)


# functions
XOpenDisplay = libX11.XOpenDisplay
XOpenDisplay.argtypes = [String]
XOpenDisplay.restype = POINTER(Display)

XCloseDisplay = libX11.XCloseDisplay
XCloseDisplay.argtypes = [POINTER(Display)]
XCloseDisplay.restype = c_int

XConnectionNumber = libX11.XConnectionNumber
XConnectionNumber.argtypes = [POINTER(Display)]
XConnectionNumber.restype = c_int

XInternAtom = libX11.XInternAtom
XInternAtom.argtypes = [POINTER(Display), String, Bool]
XInternAtom.restype = c_int

XDefaultRootWindow = libX11.XDefaultRootWindow
XDefaultRootWindow.argtypes = [POINTER(Display)]
XDefaultRootWindow.restype = Window

XCreateWindow = libX11.XCreateWindow
XCreateWindow.argtypes = [POINTER(Display), Window, c_int, c_int, c_uint, c_uint, c_uint, c_int, c_uint, POINTER(Visual), c_ulong, POINTER(XSetWindowAttributes)]
XCreateWindow.restype = Window

XDestroyWindow = libX11.XDestroyWindow
XDestroyWindow.argtypes = [POINTER(Display), Window]
XDestroyWindow.restype = c_int

XFree = libX11.XFree
XFree.argtypes = [POINTER(None)]
XFree.restype = c_int

XNextEvent = libX11.XNextEvent
XNextEvent.argtypes = [POINTER(Display), POINTER(XEvent)]
XNextEvent.restype = c_int

XPeekEvent = libX11.XPeekEvent
XPeekEvent.argtypes = [POINTER(Display), POINTER(XEvent)]
XPeekEvent.restype = c_int

XSendEvent = libX11.XSendEvent
XSendEvent.argtypes = [POINTER(Display), Window, c_int, c_long, POINTER(XEvent)]
XSendEvent.restype = c_int

XFlush = libX11.XFlush
XFlush.argtypes = [POINTER(Display)]
XFlush.restype = c_int

XPending = libX11.XPending
XPending.argtypes = [POINTER(Display)]
XPending.restype = c_int

XSynchronize = libX11.XSynchronize
XSynchronize.argtypes = [POINTER(Display), c_int]
XSynchronize.restype = POINTER(CFUNCTYPE(c_int, POINTER(Display)))


## xim
# types
class _XIC(Structure):
    pass

XIC = POINTER(_XIC)

class _XIM(Structure):
    pass

XIM = POINTER(_XIM)

class _XrmDatabase(Structure):
    pass

XrmDatabase = POINTER(_XrmDatabase)


# constants
XNInputStyle = b'inputStyle'
XNClientWindow = b'clientWindow'

XIMPreeditNothing = 0x0008
XIMPreeditNone = 0x0010
XIMStatusNothing = 0x0400
XIMStatusNone = 0x0800

XBufferOverflow = -1
NoSymbol = 0
XLookupNone = 1
XLookupChars = 2
XLookupKeySym = 3
XLookupBoth = 4


# functions
XFilterEvent = libX11.XFilterEvent
XFilterEvent.argtypes = [POINTER(XEvent), Window]
XFilterEvent.restype = c_int

XOpenIM = libX11.XOpenIM
XOpenIM.argtypes = [POINTER(Display), XrmDatabase, String, String]
XOpenIM.restype = XIM

XCloseIM = libX11.XCloseIM
XCloseIM.argtypes = [XIM]
XCloseIM.restype = c_int

XCreateIC = libX11.XCreateIC
XCreateIC.restype = XIC

XDestroyIC = libX11.XDestroyIC
XDestroyIC.argtypes = [XIC]
XDestroyIC.restype = None

XSetICFocus = libX11.XSetICFocus
XSetICFocus.argtypes = [XIC]
XSetICFocus.restype = None

Xutf8ResetIC = libX11.Xutf8ResetIC
Xutf8ResetIC.argtypes = [XIC]
Xutf8ResetIC.restype = String

Xutf8LookupString = libX11.Xutf8LookupString
Xutf8LookupString.argtypes = [XIC, POINTER(XKeyPressedEvent), String, c_int, POINTER(KeySym), POINTER(c_int)]
Xutf8LookupString.restype = c_int

XKeysymToString = libX11.XKeysymToString
XKeysymToString.argtypes = [KeySym]
XKeysymToString.restype = String

XkbKeycodeToKeysym = libX11.XkbKeycodeToKeysym
XkbKeycodeToKeysym.argtypes = [POINTER(Display), KeyCode, c_uint, c_uint]
XkbKeycodeToKeysym.restype = KeySym


## record extensions
libXtst = CDLL('libXtst.so.6')

# types
XPointer = String
XRecordContext = c_ulong
XRecordClientSpec = c_ulong

class XRecordRange8(Structure):
    _fields_ = [('first', c_ubyte),
                ('last', c_ubyte)]

class XRecordRange16(Structure):
    _fields_ = [('first', c_ushort),
                ('last', c_ushort)]

class XRecordExtRange(Structure):
    _fields_ = [('ext_major', XRecordRange8),
                ('ext_minor', XRecordRange16)]

class XRecordRange(Structure):
    _fields_ = [('core_requests', XRecordRange8),
                ('core_replies', XRecordRange8),
                ('ext_requests', XRecordExtRange),
                ('ext_replies', XRecordExtRange),
                ('delivered_events', XRecordRange8),
                ('device_events', XRecordRange8),
                ('errors', XRecordRange8),
                ('client_started', c_int),
                ('client_died', c_int)]

class XRecordInterceptData(Structure):
    _fields_ = [('id_base', XID),
                ('server_time', Time),
                ('client_seq', c_ulong),
                ('category', c_int),
                ('client_swapped', c_int),
                ('data', POINTER(c_ubyte)),
                ('data_len', c_ulong)]

XRecordInterceptProc = CFUNCTYPE(None, XPointer, POINTER(XRecordInterceptData))


# constants
XRecordAllClients = 3
XRecordFromServer = 0

# functions
XRecordAllocRange = libXtst.XRecordAllocRange
XRecordAllocRange.argtypes = []
XRecordAllocRange.restype = POINTER(XRecordRange)

XRecordCreateContext = libXtst.XRecordCreateContext
XRecordCreateContext.argtypes = [POINTER(Display), c_int, POINTER(XRecordClientSpec), c_int, POINTER(POINTER(XRecordRange)), c_int]
XRecordCreateContext.restype = XRecordContext

XRecordEnableContextAsync = libXtst.XRecordEnableContextAsync
XRecordEnableContextAsync.argtypes = [POINTER(Display), XRecordContext, XRecordInterceptProc, XPointer]
XRecordEnableContextAsync.restype = c_int

XRecordProcessReplies = libXtst.XRecordProcessReplies
XRecordProcessReplies.argtypes = [POINTER(Display)]
XRecordProcessReplies.restype = None

XRecordDisableContext = libXtst.XRecordDisableContext
XRecordDisableContext.argtypes = [POINTER(Display), XRecordContext]
XRecordDisableContext.restype = c_int

XRecordFreeContext = libXtst.XRecordFreeContext
XRecordFreeContext.argtypes = [POINTER(Display), XRecordContext]
XRecordFreeContext.restype = c_int

XRecordFreeData = libXtst.XRecordFreeData
XRecordFreeData.argtypes = [POINTER(XRecordInterceptData)]
XRecordFreeData.restype = None


## wire protocol
CARD8 = c_ubyte
CARD16 = c_ushort
CARD32 = c_uint
BOOL = CARD8
BYTE = CARD8
INT16 = c_short

class xEventType(Structure):
    _fields_ = [('type', BYTE),
                ('detail', BYTE),
                ('sequenceNumber', CARD16)]

class xKeyButtonPointer(Structure):
    _fields_ = [('pad00', CARD32),
                ('time', CARD32),
                ('root', CARD32),
                ('event', CARD32),
                ('child', CARD32),
                ('rootX', INT16),
                ('rootY', INT16),
                ('eventX', INT16),
                ('eventY', INT16),
                ('state', CARD16),
                ('sameScreen', BOOL),
                ('pad1', BYTE)]

class xEvent(Union):
    _fields_ = [('u', xEventType),
                ('keyButtonPointer', xKeyButtonPointer)]


def _kbd_wire_to_event(dpy, wev):
    ev = XEvent()
    ev.xkey.type = wev.u.type
    ev.xkey.serial = wev.u.sequenceNumber
    ev.xkey.send_event = ((wev.u.type & 0x80) != 0)
    ev.xkey.display = dpy
    ev.xkey.window = wev.keyButtonPointer.event
    ev.xkey.root = wev.keyButtonPointer.root
    ev.xkey.subwindow = wev.keyButtonPointer.child
    ev.xkey.time = wev.keyButtonPointer.time
    ev.xkey.x = wev.keyButtonPointer.eventX
    ev.xkey.y = wev.keyButtonPointer.eventY
    ev.xkey.x_root = wev.keyButtonPointer.rootX
    ev.xkey.y_root = wev.keyButtonPointer.rootY
    ev.xkey.state = wev.keyButtonPointer.state
    ev.xkey.keycode = wev.u.detail
    ev.xkey.same_screen = wev.keyButtonPointer.sameScreen
    return ev


def XWireToEvent(dpy, data):
    # this could have been avoided if _XWireToEvent didn't have internal state
    wev = cast(data, POINTER(xEvent)).contents
    if wev.u.type in [KeyPress, KeyRelease]:
        return _kbd_wire_to_event(dpy, wev)
    return XEvent(wev.u.type)
