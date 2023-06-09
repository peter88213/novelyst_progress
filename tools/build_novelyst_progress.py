"""Build a collection novelyst plugin.
        
In order to distribute a single script without dependencies, 
this script "inlines" all modules imported from the pywriter package.

The PyWriter project (see https://github.com/peter88213/PyWriter)
must be located on the same directory level as the novelyst_progress project. 

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_progress
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys
sys.path.insert(0, f'{os.getcwd()}/../../PyWriter/src')
import inliner

SRC = '../src/'
BUILD = '../test/'
SOURCE_FILE = f'{SRC}novelyst_progress.py'
TARGET_FILE = f'{BUILD}novelyst_progress.py'


def main():
    inliner.run(SOURCE_FILE, TARGET_FILE, 'nvprogresslib', '../../novelyst_progress/src/')
    inliner.run(TARGET_FILE, TARGET_FILE, 'novelystlib', '../../novelyst/src/')
    inliner.run(TARGET_FILE, TARGET_FILE, 'pywriter', '../../PyWriter/src/')
    print('Done.')


if __name__ == '__main__':
    main()
