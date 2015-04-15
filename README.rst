=====================
Screencast your keys.
=====================

A screencast tool to display your keys; forked from screenkey_ 0.2, inspired by
Screenflick_ and initially based on key-mon_.


Main changes from screenkey 0.2
-------------------------------

- Multi-monitor support
- Configurable size/position
- Can show modifier sequences only
- Improved backspace processing (3 different modes)
- Normal/Emacs/Mac caps modes
- Enable/disable dynamically by pressing both control keys
- All settings available through command-line flags
- Usable without system tray (for tiling window managers)
- Several bug fixes


Usage
-----

Execute without installation::

  ./screenkey

To install::

  sudo ./setup.py install

Dependencies:

- PyGTK
- setuptools (build only)
- DistUtils-Extra (build only)

Install dependencies (on Debian/Ubuntu)::

  sudo apt-get install python-gtk2 python-setuptools python-distutils-extra


Advanced usage
--------------

Overlay on top of an existing window, interactive selection using slop_:

  ./screenkey -g $(slop -n -f '%g')

Set actual text rectangle interactively (drag during selection):

  ./screenkey -p fixed -g $(slop -n -f '%g')

Record an Emacs screencast:

  ./screenkey --mods-mode emacs -s small -g $(slop -n -f '%g')

Persistent window:

  ./screenkey --persist

Press both control keys during a recording to disable screenkey (for example,
during password prompts). Press both again to resume screenkey.

To get transparency you need a compositor to be running (for example, "compton"
or "unagi").


Authors and Copyright
---------------------

"screenkey" can be found at https://github.com/wavexx/screenkey

| "screenkey" is distributed under GNU GPLv3+, WITHOUT ANY WARRANTY.
| Copyright(c) 2010-2012 Pablo Seminario <pabluk@gmail.com>
| Copyright(c) 2015 by wave++ "Yuri D'Elia" <wavexx@thregr.org>.


Additional Thanks
-----------------

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
