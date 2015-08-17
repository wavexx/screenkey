=====================
Screencast your keys.
=====================

.. contents::

A screencast tool to display your keys inspired by Screenflick_.
This is an almost-complete rewrite of screenkey_ 0.2, featuring:

- Several keyboard translation methods
- Key composition/input method support
- Configurable font/size/position
- Highlighting of recent keystrokes
- Improved backspace processing
- Normal/Emacs/Mac caps modes
- Multi-monitor support
- Dynamic recording control by pressing both control keys
- Switch for visible shift and modifier sequences only
- Countless bug fixes


Installation and basic usage
----------------------------

Execute without installation::

  ./screenkey

To install::

  sudo ./setup.py install

Dependencies:

- Python 2.7 (Python 3 support yet incomplete)
- PyGTK
- setuptools (build only)
- DistUtils-Extra (build only)

Install dependencies (on Debian/Ubuntu)::

  sudo apt-get install python-gtk2 python-setuptools python-distutils-extra

You can also install "screenkey" via ArchLinux's AUR package:

https://aur.archlinux.org/packages/screenkey


Settings
--------

Display time:
  Persistence (in seconds) of the output window after typing has stopped.
  Defaults to 2.5 seconds.

Persistent window:
  Forces the output window to be always visible, irregardless of typing
  activity. Mostly useful for interactive window placement and/or "fixed"
  positioning.

Font:
  Font used for the output window. A scalable font and wide Unicode coverage is
  required (the DejaVu family is *highly* recommended).

Screen:
  Physical screen/monitor used for the output window.

Position:
  Position of the output window. If "fixed" is chosen, the output window's
  position and size can be either specified on the command line or changed
  interactively (see `Interactive placement`_).

Size:
  Size of the font used in the output window. Chooses proportionally between
  8/12/24% of the screen size. When "fixed" positioning is used, size is
  ignored and the font will fill the available height of the output window.

Keyboard mode:
  Choose the translation method of keyboard events.

  "Composed" attempts to show only the final results of key composition. Dead
  keys and any intermediate output during composition is not shown. Currently
  works correctly with XIM/IBUS, but only for on-the-spot editing. It can cause
  problems with complex input methods (support for wider compatibility is
  underway).

  "Translated" shows the result of each keypress on the keyboard, accounting
  for the current keyboard locale and modifiers, but not composition. Pressing
  a dead key followed by a letter will show both keys.

  "Raw" shows which key caps were pressed on the keyboard, without translation.
  For example, the key "!" which is often located on the "1" key, requires
  pressing "Shift+1", which is what this output mode shows. "Backspace mode",
  "Always visible Shift" and "Modifiers only" have no effect in this mode.

  "Keysyms" shows the keysyms ("symbolic" names) of each pressed key as
  received by the server. Mostly useful for debugging.

Backspace mode:
  Controls the effect of "backspace" on the text in the output window.

  "Normal" always inserts a backspace symbol in the output window.

  "Baked" simulates the effect of backspace in the text only if the last
  keypress is a regular letter and no caret movement has been detected. In any
  other case, a backspace symbol is inserted instead.

  "Full" is similar to "baked", but will eat through several other, less safe
  keys, such as tabs and returns.

Modifiers mode:
  Select how modifiers keys (such as Control, Alt) are displayed in the output
  window. "Normal" uses traditional PC names while "Mac" uses Mac symbols
  directly. The "Emacs" mode will display Emacs-style shortened keyboard
  sequences.

Modifiers only:
  Only show modifier/control sequences in the output window.
  Bare, shifted or translated letters are not shown.

Always show Shift:
  Shift is normally hidden when the control sequence includes a letter that can
  differentiate between a shifted/non-shifted key. For example, Shift +
  "Control+a" is normally shown just as "Control+A" (notice the capital "A").

  When "Always show Shift" is used, Shift is always included in modifier
  sequences, if pressed. Has no effect when using the "Emacs" modifiers mode.


Advanced usage
--------------

Controlling visibility
~~~~~~~~~~~~~~~~~~~~~~

Press both control keys during a recording to disable screenkey (for example,
during password prompts). Press both again to resume it.

If you need the viewer to focus on a sentence you just typed, you can press a
silent modifier (such as Shift, or Control) to keep the output window visible a
bit longer.


Interactive placement
~~~~~~~~~~~~~~~~~~~~~

screenkey in "fixed" positioning mode allows its window to be resized and
placed as you see fit. You can provide the geometry on the command line, but
you can also move and resize it dynamically.

To perform this task, toggle "Persistent window" first so that the window
no longer disappears, then select "Fixed" from the position drop-down.

Since the window has no borders, the actual resizing method depends on the
window manager and might vary a bit. Most window managers allow to resize any
window by holding down the Alt (or Win) key and dragging with the third mouse
button next to the corner of a window.

Move the mouse next to the corner that you want to resize, hold down Alt, hold
down the third (right) mouse button and drag in the direction you want.

After the window has been resized, toggle again "Persistent window" to restore
the original behavior.


Command-line placement
~~~~~~~~~~~~~~~~~~~~~~

The "geometry" argument follows the standard X11 geometry format
(``WxH[+X+Y]``) and can be provided by slop_, which allows to select windows
and/or drag the desired region interactively without calculating the
coordinates manually.

When a geometry argument has been provided, the position (top/middle/bottom)
becomes relative to the selected rectangle. For example, to overlay screenkey
on top of an existing window, you can simply do::

  ./screenkey -g $(slop -n -f '%g')

To set the actual text rectangle instead, use "fixed" positioning. Using slop,
you can combine both and simply drag the desired rectangle during selection::

  ./screenkey -p fixed -g $(slop -n -f '%g')


Choosing a good font
~~~~~~~~~~~~~~~~~~~~

The default font is "Sans Bold", which is usually mapped to "DejaVu Sans" on
most Linux installations (look for the ``ttf-dejavu`` package). It's a good
all-around font which provides all the required glyphs and has *excellent*
readability.

For screencasts about programming, we recommend "DejaVu Sans Mono Bold"
instead, which provides better differentiation among similar letterforms (0/O,
I/l, etc).


Tiling window managers
~~~~~~~~~~~~~~~~~~~~~~

"screenkey" should work correctly by default with tiling window managers.

If you don't have a system tray, you can either configure it through command
line flags or use ``--show-settings`` to test the configuration interactively.

To get transparency you need a compositor to be running. For example, "compton"
or "unagi" are popular for their low impact on performance, but "xcompmngr"
also works correctly without any additional configuration.


Related tools
~~~~~~~~~~~~~

If you're recording a screencast where almost all editing is already visible
(for example, in ``vi`` or most other text editors), consider using a bigger
screen font instead, letting the viewer read the text directly on the real
program.

If the control sequences you're typing are rare, you might even want to spell
what you're doing instead of obscuring the screen with the typing output.

When doing screencasts involving a lot of mouse activity, or which require
holding down modifiers to perform other mouse actions, key-mon_ might be a good
companion to screenkey, or replace it entirely.

key-mon can be configured to show the state of key modifiers continuously and
circle the location of mouse clicks ("visible click"). key-mon and screenkey
complete each-other and can be used at the same time.


Authors and Copyright
---------------------

"screenkey" can be found at https://github.com/wavexx/screenkey

| "screenkey" is distributed under GNU GPLv3+, WITHOUT ANY WARRANTY.
| Copyright(c) 2010-2012 Pablo Seminario <pabluk@gmail.com>
| Copyright(c) 2015 by wave++ "Yuri D'Elia" <wavexx@thregr.org>.


Additional Thanks
-----------------

* Benjamin Chrétien
* Doug Patti
* Ivan Makfinsky
* Jacob Gardner
* Muneeb Shaikh
* farrer (launchpad)
* zhum (launchpad)


.. _screenkey: https://launchpad.net/screenkey
.. _Screenflick: http://www.araelium.com/screenflick/
.. _key-mon: https://code.google.com/p/key-mon/
.. _slop: https://github.com/naelstrof/slop
