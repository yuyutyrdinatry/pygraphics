import os
import sys
from config import *
from content import OS_CURR, OS_WIN, OS_MAC, OS_ALL
from subprocess import call

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
        
        # Windows
        self._create_windows_installer()
        self._build_windows_installer()
    
    #-------------------------------------- Windows Installer Generation Helpers
    def _build_windows_installer(self):
        make = os.path.join(WIN_PATH_NSIS, 'makensis.exe')
        call('%s "%s"' % (make, NSIS_BUILD))
        
    def _create_windows_installer(self):
        f = open(NSIS_BUILD, 'w')
        
        f.write(self._get_header())
        f.write('\n')
        f.write(self._get_sections())
        f.write('\n')
        f.write(self._get_footer())
        f.close()
        
    def _get_sections(self):
        sections = '\n; Sections'
        main_str = 'SetOutPath "$INSTDIR"'
        u_str = 'WriteUninstaller "$INSTDIR\Uninstall.exe"'
        
        for obj in self.DO.data_objs[OS_WIN]:
            new_section = '''\n    Section "%(SEC_NAME)s" %(SEC_ID)s
        %(MAIN)s
        %(FILES)s
        %(UNINSTALL)s
    SectionEnd\n''' % {'SEC_NAME' : obj.name, 
                       'MAIN' : main_str, 
                       'UNINSTALL' : u_str, 
                       'SEC_ID' : obj.name.replace(' ', ''),
                       'FILES' : self._get_files(obj)}
            sections = '%s%s' % (sections, new_section)
            main_str = ''
            u_str = ''
        
        return sections
    
    def _get_files(self, obj):
        return ';Files\n'
    
    def _get_header(self):
        f = open(os.path.join(PATH_CWD, 'RES', '_nsis_header.nsi'))
        return f.read()
    
    def _get_footer(self):
        footer = '''; General
    Name "%(NAME)s"
    OutFile "DIST/%(FILENAME)s.exe"
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
            self._remove_files(path, files)
            
            for dir in dirs:
                self._delete(dir)
                
            self._remove_path(path)
        
    def _remove_files(self, path, files):
        for file in files:
            os.remove(os.path.join(path, file))
    
    def _remove_path(self, path):
        os.rmdir(path)