class DataObjects(object):
    def __init__(self):
        self.data_objs = {}
    
    def add_data(self, name, path, os, **kwargs):
        if not os in self.data_objs:
            self.data_objs[os] = []
             
        self.data_objs[os].append(iDataObj(name, path, os, **kwargs))

class iDataObj(object):
    def __init__(self, name, path, os, recurse=False, cmds={}, main=False):
        self.name = name
        self.os = os
        self.path = path
        self.recurse = recurse
        self.contents = path
        self.cmds = cmds
        self.main = main
        
        self._trav_path()
        
    def _trav_path(self):
        p = self.path
        self.contents = None