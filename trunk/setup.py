# -*- coding: utf-8 -*-
import sys
import py2exe
import os

if sys.platform == 'win32':
    from distutils.core import setup
    origIsSystemDLL = py2exe.build_exe.isSystemDLL
    def isSystemDLL(pathname):
            if os.path.basename(pathname).lower() in ("qlcoverflow.dll.dll"):
                    return 0
            return origIsSystemDLL(pathname)
    py2exe.build_exe.isSystemDLL = isSystemDLL

    setup(
        name='imguploader',
        windows=[{'script':'main.py' ,  'icon_resources': [(1, "img/icon.ico")]}],
        options = { "py2exe" :
                            {"includes" : ["sip", "PictureFlow"],
                            "dist_dir" : "dist",
                            "optimize":2,
                            "excludes":["_ssl"],
                            "compressed":True,
                            }}
        )

elif sys.platform == 'darwin':
    from setuptools import setup
    APP = ['main.py']
    OPTIONS = {'argv_emulation': True, 'includes': ['sip', 'BeautifulSoup', 'PictureFlow', 'ImageQt'], 'plist':{'CFBundleDocumentTypes':[], 'CFBundleGetInfoString':'Image uploader'},'iconfile':'PythonApplet.icns'}
    
    setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    )
