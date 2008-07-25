import os
import sys
from config import *

PATH_CWD = os.getcwd()
PATH_BUILD = os.path.join(PATH_CWD, 'BUILD')
PATH_DIST = os.path.join(PATH_CWD, 'DIST')

NSIS_BUILD = os.path.join(PATH_CWD, 'BUILD.nsi')

class InstallerBuilder(object):
    def __init__(self, data_objects):
        self.DO = data_objects
        
    def generate(self):
        self._clear_build_paths()
        self._create_build_paths()
        self._create_windows_installer()
        
    def _create_windows_installer(self):
        if os.path.exists(NSIS_BUILD):
            os.rmdir(NSIS_BUILD)
        
        f = open(NSIS_BUILD, 'w+')
        
        header = self._get_header()
        footer = self._get_footer()
        
        f.write(header)
        f.write(footer)
        f.close()
    
    #-------------------------------------- Windows Installer Generation Helpers
    def _get_header(self):
        f = open(os.path.join(PATH_CWD, '_nsis_header.nsi'))
        return f.readlines()
    
    def _get_footer(self):
        footer = '''; General
    Name "%(NAME)s"
    OutFile "BUILD/%(FILENAME)s.exe"
    InstallDir "%(INSTALL_DIR)s"
    RequestExecutionLevel user
        ''' % {'NAME' : INST_NAME, 'FILENAME' : INST_FILE, 
               'INSTALL_DIR' : WIN_PATH_DEFAULT_INSTALL}
        return footer
    
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
            print path, dirs, files
            self._remove_files(path, files)
            
            for dir in dirs:
                self._delete(dir)
                
            self._remove_path(path)
        
    def _remove_files(self, path, files):
        for file in files:
            print 'remove', path, file, os.path.join(path, file)
            os.remove(os.path.join(path, file))
    
    def _remove_path(self, path):
        print 'rmdir', path
        os.rmdir(path)