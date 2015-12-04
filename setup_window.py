# setup.py -- py to exe

from distutils.core import setup
import py2exe
import zipfile
import datetime

options = {
    "includes": ["sip", ],
    "dll_excludes": ["MSVCP90.dll", ],
    "compressed": 1,
    "optimize": 2,
    "ascii": 0,
    "bundle_files": 1
}

setup(
    windows=[{'script': 'init_window.pyw'}],
    zipfile=None,
    options={'py2exe': options},
    script_args=["py2exe"],
)

date = datetime.datetime.now().strftime("[%y%m%d]")
zipname = "dist/" + date + "[W]FileTagger.zip"

f = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
f.write("dist/init_window.exe", "FileTagger.exe")

# py2exe扫描不到这个dll, 无法把它打包进exe里
# pyinstaller可以, 但生成exe过大(超过20mb), 且打开较慢
f.write("ui/qwindows.dll", "platforms/qwindows.dll")

f.close()
