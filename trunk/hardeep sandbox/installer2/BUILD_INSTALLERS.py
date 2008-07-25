# Builds the installers.
# Do NOT modify this file unless you know what you are doing!

import os
import sys
from config import *
from content import *

for os in DO.data_objs:
    print os
    for cmd in DO.data_objs[os]:
        print cmd
        
# Begin Windows Installer Generation
#!include MUI2.nsh

class InstallerBuilder(object):
    PATH_CWD = os.getcwd()
    PATH_BUILD = os.path.join(CUR_PATH, 'BUILD')
    PATH_DIST = os.path.join(CUR_PATH, 'DIST')
    
    NSIS_INSTALL_FILE = os.path.join() 
    
    def __init__(self, data_objects):
        self.DO = data_objects
        
    def generate(self):
        self._clear_build_paths()
        self._create_build_paths()
        self._create_windows_installer()
        
    def _create_windows_installer(self):
        header = self._get_header()
    
    #-------------------------------------- Windows Installer Generation Helpers
    def _get_header(self):
        f = open(os.path.join(PATH_CWD, '_nsis_header.nsi'))
        return f.readlines()
    
    #---------------------------------------------------------- File/Dir Helpers
    def _clear_build_paths(self):
        if os.path.exists(PATH_BUILD):
            self._delete(PATH_BUILD)
            
        if os.path.exists(PATH_DIST):
            self._delete(PATH_DIST)
            
    def _create_build_paths(self):
        os.mkdir(PATH_BUILD)
        os.mkdir(PATH_DIST)
            
    def _delete(self, delete_dir):
        for path, dirs, files in os.walk(delete_dir):
            os._remove_files(path, files)
            os._remove_path(path)
        
    def _remove_files(self, path, files):
        for file in files:
            os.remove(os.path.join(path, file))
    
    def _remove_path(self, path):
        os.rmdir(path)