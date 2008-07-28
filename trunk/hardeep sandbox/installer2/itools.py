class DataObjects(object):
    def __init__(self):
        self.data_objs = {}
    
    def add_data(self, name, path, os, **kwargs):
        if not os in self.data_objs:
            self.data_objs[os] = []
             
        self.data_objs[os].append(iDataObj(name, path, os, **kwargs))

class iDataObj(object):
    def __init__(self, name, path, os, recurse=False, cmds={}, required=False):
        self.name = name
        self.os = os
        self.path = path
        self.recurse = recurse
        self.contents = path
        self.cmds = cmds
        self.is_required = required