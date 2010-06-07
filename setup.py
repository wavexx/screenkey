#!/usr/bin/env python

from distutils.core import setup

setup(
    name = 'screenkey',
    version = '0.1.1',
    packages = ['Screenkey'],
    package_dir = {'Screenkey': 'Screenkey'},
    data_files = [('/usr/share/applications', ['data/screenkey.desktop'])],
    scripts=['screenkey'],
    author='Pablo Seminario',
    author_email='pabluk@gmail.com',
    platforms=['POSIX'],
    license='GPLv3',
    keywords='screencast keyboard keys',
    url='http://launchpad.net/screenkey',
    download_url='http://launchpad.net/screenkey/+download',
    description='A screencast tool to display keys',
    long_description="""
    Screenkey is a useful tool for presentations or screencasts.
    Inspired by ScreenFlick and based on the key-mon project code.
    """,
)
