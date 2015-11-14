# setup.py -- py to exe

from distutils.core import setup
import sys
import glob
import py2exe
import os


options = {"py2exe": {"bundle_files": 1}}


setup(console=["init_cmd.py"], options=options,
      zipfile=None, script_args=["py2exe"])
