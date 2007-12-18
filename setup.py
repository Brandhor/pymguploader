from distutils.core import setup
import py2exe
import os

setup(
    name='imguploader',
    windows=[{'script':'main.py' }],
    options = { "py2exe" : {"includes" : "imgsite.imagecross, PyQt4._qt, sip", "dist_dir" : "dist", "optimize":2}}
    )
