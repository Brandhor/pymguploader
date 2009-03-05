from distutils.core import setup
import py2exe
import os

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
