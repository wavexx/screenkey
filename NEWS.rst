screenkey 0.9
-------------

- Ctrl+Ctrl detection now works correctly in more scenarios.
- Ctrl++ (and similar sequences with repeated characters) are now shown as
  Ctrl+"+" for improved readability.
- Shift+Backspace is now recognized and shown correctly.
- Several multimedia keys are now supported. If "FontAwesome" is installed,
  the correct symbol is also displayed instead of a text abbreviation.
- Visualization of whitespace characters can now be controlled.
- Repeated key sequences are now abbreviated with a repeat count if above the
  specified threshold (3 by default).


screenkey 0.8.1
---------------

- Fixed startup issue in Ubuntu without using ``--no-detach``.
- Fixed desktop menu file.


screenkey 0.8
-------------

- Fix Alt+Shift mapping on stock altgr-intl keyboard layouts.
- Correctly stay above fullscreen windows.
- Do not mask pointer/keyboard events: allow the mouse to be used normally
  "under" the output window.
- Improved interactive positioning (slop is required).
- Allow KeySyms to be ignored (added ``--ignore`` on the command line), for
  better interaction with custom keyboard maps.


screenkey 0.7
-------------

- Font color, background color and opacity are now fully configurable.
- The saved state of boolean settings (persistent, modifiers only, etc) is
  correctly restored when changed from the settings dialog.


screenkey 0.6.2
---------------

- HiDPI support
- Fix initial state of "Persistent window" in the preferences.
- Allow to reset the stored the geometry from the preferences also when
  changed interactively.


screenkey 0.6.1
---------------

- Fix exception on first run.


screenkey 0.6
-------------

- The ``python-xlib`` module and the ``xmodmap`` executable are not
  required/used anymore. screenkey now uses ``libX11.so.6`` directly.
- Key composition/input method support.
- A new setting (always show Shift) has been added to always add "Shift" in
  modifier sequences which contain capitalizable letters.
- CapsLock and NumLock status (on/off) is now shown when pressed.


screenkey 0.5
-------------

- Fixes issues with recent ``glib`` versions.
- ``XAUTHORITY`` is no longer required to be set.


screenkey 0.4
-------------

- The font is now configurable as well
- Tweaks to symbol spacing
- Highlight recent keypresses for improved readability


screenkey 0.3
-------------

- Multi-monitor support
- Configurable size/position
- Can show modifier sequences only
- Improved backspace processing (3 different modes)
- Normal/Emacs/Mac caps modes
- Enable/disable dynamically by pressing both control keys
- All settings available through command-line flags
- Usable without system tray (for tiling window managers)
- Several bug fixes
