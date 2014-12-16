from distutils.core import setup
import py2exe
import sys

sys.path.append( "c:\\python27\\Lib\\site-packages\\gtk2.16.6" )

setup( console = [ 'washClient.py' ],
	 options={
                "py2exe":{
                        "unbuffered": True,
                        "optimize": 2,
                        "packages": [ "twisted", "gtk", "webkit", "cairo",
                                    "pango", "pangocairo", "atk", "gobject",
                                    "gio" ]
                                    ,
                        "dll_excludes": [ "libgthread-2.0-0.dll",
                                        "libglib-2.0-0.dll",
                                        "libwebkit-1.0-2.dll",
                                        "libgtk-win32-2.0-0.dll",
                                        "libgobject-2.0-0.dll",
                                         "libffi-5.dll",
                                         "libglade-2.0-0.dll",
                                         "intl.dll",
                                         "libgdk-win32-2.0-0.dll",
                                         "libgio-2.0-0.dll",
                                         "libgdk_pixbuf-2.0-0.dll",
                                         "libcairo-2.dll",
                                         "libpango-1.0-0.dll",
                                         "libatk-1.0-0.dll",
                                         "libpangocairo-1.0-0.dll"
                                        ]
                }
        }
 )
