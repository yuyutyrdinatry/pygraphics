import os
import sys
from config import *
from content import OS_CURR, OS_WIN, OS_MAC, OS_ALL
from subprocess import call
import re

#===============================================================================
# Globals
#===============================================================================
PATH_CWD = os.getcwd()
PATH_BUILD = os.path.join(PATH_CWD, 'BUILD')
PATH_DIST = os.path.join(PATH_CWD, 'DIST')

NSIS_BUILD = os.path.join(PATH_CWD, 'BUILD', 'BUILD.nsi')
NSIS_CMD_LINE_TOOL = os.path.join(WIN_PATH_NSIS, 'makensis.exe')

class InstallerBuilder(object):
    def __init__(self, data_objects):
        self.DO = data_objects
        
    def generate(self):
        self._clear_build_paths()
        self._create_build_paths()
        
        # Windows
        self._create_windows_build_file()
        self._build_windows_installer()
        
        #self._move_to_dist()
        
    def _move_to_dist(self):
        win_file = '%s.exe' % INST_FILE
        os.rename(os.path.join(PATH_BUILD, win_file), 
                  os.path.join(PATH_DIST, win_file))
        
    def _parse_cmd(self, cmd):
        split = cmd.split('::')
        
        # Delete a file
        if split[0] == 'DEL':
            return 'Delete "%s"' % split[1]
        
        # Add a str to an environment variable (WINDOWS ONLY)
        if split[0] == 'ENV':
            # See:
            # http://nsis.sourceforge.net/Path_Manipulation#Usage
            cmd = '        ${EnvVarUpdate} $0 "%s" "%s" "HKLM" "%s"\n' % (split[2], split[1], split[3])
            cmd += '        SetRebootFlag true\n'
            return cmd 
        
        return ''
    
    def _process_python_module(self, obj, sec_name):
        try:
            os.mkdir(os.path.join(PATH_BUILD, sec_name))
        except:
            pass
        
        the_cmd = 'python "%s" build --build-base="%s"' % (os.path.join(obj.path, 'setup.py'), os.path.join(PATH_BUILD, sec_name))
        
        # For windows...
        build_cmd = ''
        build_cmd += 'cd %s\n' % os.sep
        build_cmd += 'cd %s\n' % obj.path
        build_cmd += the_cmd
        
        bat_file = open(os.path.join(PATH_BUILD, sec_name + '.bat'), 'w')
        bat_file.write(build_cmd)
        bat_file.close()
        
        call(os.path.join(PATH_BUILD, sec_name + '.bat'))
        base_folder = os.path.join(PATH_BUILD, sec_name)
        contents = os.listdir(base_folder)
        
        obj.path = os.path.join(PATH_BUILD, sec_name, contents[0])
        lib_contents = os.listdir(obj.path)
        for item in lib_contents:
            if os.path.isdir(os.path.join(base_folder, item)):
                path_file = open(os.path.join(base_folder, item + '.pth'), 'w')
                path_file.write(item)
                path_file.close()
    
    #-------------------------------------- Windows Installer Generation Helpers
    def _build_windows_installer(self):
        call('%s "%s"' % (NSIS_CMD_LINE_TOOL, NSIS_BUILD))
        
    def _create_windows_build_file(self):
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
        ; Enable Logging
        ;    LogSet on
    SectionEnd\n'''
        sections = '%s%s' % (sections, new_section)
        
        for obj in self.DO.data_objs[OS_WIN]:
            sections = '%s%s' % (sections, self._get_section_code(obj))
            
        for obj in self.DO.data_objs[OS_ALL]:
            sections = '%s%s' % (sections, self._get_section_code(obj))
            
        return sections
    
    def _get_section_code(self, obj):
        sec_name = self._get_section_id_from_name(obj.name)
        
        if obj.cmds.has_key('PYTHON_MODULE_SRC'):
            self._process_python_module(obj, sec_name)
        
        new_section = '''\n    Section "%(SEC_NAME)s" %(SEC_ID)s
        %(FILES)s
        %(COMMANDS)s
        %(REQ)s
    SectionEnd\n''' % {'SEC_NAME' : obj.name,  
                       'SEC_ID' : sec_name,
                       'FILES' : self._get_files(obj, sec_name),
                       'COMMANDS' : self._get_commands(obj),
                       'REQ' : 'SectionIn RO' if obj.is_required else ''}
        return new_section
    
    def _get_section_id_from_name(self, name):
        p = re.compile('(\s|\W|_)*')
        return p.sub('', name)
    
    def _get_files(self, obj, sec_name):
        files = '; Files\n'
        if not obj.recurse:
            
            # Single File
            if os.path.isfile(obj.path):
                files = '%s        File "%s"\n' % (files, obj.path)
            
            # Folder (no sub folders included) 
            elif os.path.isdir(obj.path):
                for file in listdir(obj.path):
                    if os.path.isfile(file):
                        files = '%s        File "%s"\n' % (files, obj.path)
        
        elif os.path.isdir(obj.path):
            # All files and folders in the given path. Given path MUST be a
            # folder!
            if obj.cmds.has_key('PYTHON_MODULE_SRC'):
                files = '%s        SetOutPath "$INSTDIR\python\Lib\site-packages"\n' % files
            elif obj.cmds.has_key('PYTHON_DATA_COPY'):
                files = '%s        SetOutPath "$INSTDIR\python"\n' % files
            else:
                files = '%s        SetOutPath "$INSTDIR\%s"\n' % (files, sec_name)
                
            out_path = ''
            for p_path, p_dirs, p_files in os.walk(obj.path):
                
                cur_path = p_path.replace(obj.path, '')
                if out_path is not cur_path:
                    out_path = cur_path
                    
                    if obj.cmds.has_key('PYTHON_MODULE_SRC'):
                        files = '%s        SetOutPath "$INSTDIR\python\Lib\site-packages%s"\n' % (files, out_path)
                    elif obj.cmds.has_key('PYTHON_DATA_COPY'):
                        files = '%s        SetOutPath "$INSTDIR\python%s"\n' % (files, out_path)
                    else:
                        files = '%s        SetOutPath "$INSTDIR\%s%s"\n' % (files, sec_name, out_path)
                     
                for file in p_files:
                    file_path = os.path.join(p_path, file)
                    files = '%s        File "%s"\n' % (files, file_path)

            files = '%s        SetOutPath "$INSTDIR"\n' % files
        else:
            raise ValueError('Invalid Value for [%s].path -> %s' % (obj.name, 
                                                                    obj.path))
                
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
                    
            elif c == 'post_install':
                if isinstance(obj.cmds[c], list):
                    for cmd in obj.cmds[c]: 
                        cmds = '%s        %s\n' % (cmds, self._parse_cmd(cmd))
                else:
                    cmds = '%s        %s\n' % (cmds, self._parse_cmd(obj.cmds[c]))
                    
            elif c == 'PYTHON_MODULE_SRC':
                print "SET Module To Copy On Install"
                
            elif c == 'PYTHON_DATA_COPY':
                print "SET Direct copy to python folder"
            
            else:
                print 'Unknown Command: %s -> %s' % (c, obj.cmds[c])  
                
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
        print '------', delete_dir
        for path, dirs, files in os.walk(delete_dir):
            print 'rem', path, files
            self._remove_files(path, files)
            
            for dir in dirs:
                print 'del', dir
                self._delete(os.path.join(delete_dir, dir))
                
            print 'self', path
            self._remove_path(path)
        
    def _remove_files(self, path, files):
        for file in files:
            print '\t rem_file', os.path.join(path, file) 
            os.remove(os.path.join(path, file))
    
    def _remove_path(self, path):
        os.rmdir(path)