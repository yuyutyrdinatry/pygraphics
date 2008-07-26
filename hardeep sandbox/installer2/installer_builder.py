import os
import sys
from config import *
from content import OS_CURR, OS_WIN, OS_MAC, OS_ALL
from subprocess import call

PATH_CWD = os.getcwd()
PATH_BUILD = os.path.join(PATH_CWD, 'BUILD')
PATH_DIST = os.path.join(PATH_CWD, 'DIST')

NSIS_BUILD = os.path.join(PATH_CWD, 'BUILD', 'BUILD.nsi')

class InstallerBuilder(object):
    def __init__(self, data_objects):
        self.DO = data_objects
        
    def generate(self):
        self._clear_build_paths()
        self._create_build_paths()
        
        # Windows
        self._create_windows_installer()
        self._build_windows_installer()
        
        self._move_to_dist()
        
    def _move_to_dist(self):
        win_file = '%s.exe' % INST_FILE
        os.rename(os.path.join(PATH_BUILD, win_file), 
                  os.path.join(PATH_DIST, win_file))
        
    def _parse_cmd(self, cmd):
        split = cmd.split('::')
        
        # Delete a file
        if split[0] == 'DEL':
            return 'Delete "%s"' % split[1]
        
        # Add a str to an environment variable
        if split[0] == 'ENV':
            
            cmd = '        ${EnvVarUpdate} $0 "%s" "%s" "HKLM" "%s"\n' % (split[2], split[1], split[3])
            cmd += '        SetRebootFlag true\n'
##            cmd = '\n'
##            cmd += '        ReadRegStr $0 HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment" \'%s\'\n' % split[1]
##            #C:\Program Files\ActiveState Komodo Edit 4\;c:\ruby\bin;%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;c:\Python25\;c:\ruby;C:\Program Files\3DPaintBrush\;C:\Program Files\QuickTime\QTSystem\
##            cmd += '        WriteRegStr HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment" \'%s\' \'%s\'\n' % (split[2], '$0' + split[3])
##            cmd += '        Pop $0\n'
##            cmd += '        SetRebootFlag true\n'
            return cmd 
        
        return ''
    
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
        
        new_section = '''\n    Section "-Settings"
        SetOutPath "$INSTDIR"
        WriteUninstaller "$INSTDIR\Uninstall.exe"
    SectionEnd\n'''
        sections = '%s%s' % (sections, new_section)
        
        for obj in self.DO.data_objs[OS_WIN]:
            new_section = '''\n    Section "%(SEC_NAME)s" %(SEC_ID)s
        %(FILES)s
        %(COMMANDS)s
        %(REQ)s
    SectionEnd\n''' % {'SEC_NAME' : obj.name,  
                       'SEC_ID' : obj.name.replace(' ', ''),
                       'FILES' : self._get_files(obj),
                       'COMMANDS' : self._get_commands(obj),
                       'REQ' : 'SectionIn RO' if obj.is_required else ''}
            sections = '%s%s' % (sections, new_section)
        
        return sections
    
    def _get_files(self, obj):
        files = ';Files\n'
        if not obj.recurse:
            
            # Single File
            if os.path.isfile(obj.path):
                files = '%s        File "%s"\n' % (files, obj.path)
                
        return files
    
    def _get_commands(self, obj):
        cmds = '; Commands\n'
        for c in obj.cmds:
            
            if c == 'nsis_install':
                if isinstance(obj.cmds[c], list):
                    for cmd in obj.cmds[c]: 
                        cmds = '%s        %s\n' % (cmds, "ExecWait '%s'" % cmd)
                else:
                    cmds = '%s        %s\n' % (cmds, "ExecWait '%s'" % obj.cmds[c])
                    
            if c == 'post_install':
                if isinstance(obj.cmds[c], list):
                    for cmd in obj.cmds[c]: 
                        cmds = '%s        %s\n' % (cmds, self._parse_cmd(cmd))
                else:
                    cmds = '%s        %s\n' % (cmds, self._parse_cmd(obj.cmds[c]))
                
        return cmds
    
    def _get_header(self):
        f = open(os.path.join(PATH_CWD, 'RES', '_nsis_header.nsi'))
        return f.read()
    
    def _get_footer(self):
        footer = '''; General
    Name "%(NAME)s"
    OutFile "%(FILENAME)s.exe"
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