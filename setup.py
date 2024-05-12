from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {
        'bundle_files': 1,  # Bundle everything including the Python interpreter
        'compressed': True  # Compress the library archive
    }},
    windows = [{'script': "MainWorking.py"}],
    zipfile = None,  # Include the library files in the executable itself
    packages=['data', 'images'],
    data_files = [('data', ['archer.db']),
                  ('images', ['img_1.png'])]  # Directory and files to include
)