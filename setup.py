# setup.py -- pack py to single exe

from distutils.core import setup
import py2exe
import zipfile
import datetime

options = {
    "compressed": 1,
    "optimize": 2,
    "ascii": 0,
    "bundle_files": 1
}


setup(
    console=["init_cmd.py"],
    options={'py2exe': options},
    zipfile=None,
    script_args=["py2exe"]
)

date = datetime.datetime.now().strftime("[%y%m%d]")
zipname = "dist/" + date + "[C]FileTagger.zip"

f = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
f.write("dist/init_cmd.exe", "FileTagger.exe")
f.close()
