from distutils.core import setup
import py2exe
import os

setup(
    name='imguploader',
    windows=[{'script':'main.py' ,  'icon_resources': [(1, "img/icon.ico")]}],
    options = { "py2exe" : {"includes" : "PyQt4._qt, sip", "dist_dir" : "dist", "optimize":2}}
    )
