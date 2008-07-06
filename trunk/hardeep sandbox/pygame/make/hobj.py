import pygame

class hObj(object):
    
    def __init__(self, name='obj', **kwargs):
        '''
        Keywords accepted:
        '''
        self.__init_vars()
        
        self.name = name
        
    def __init_vars(self):
        self.look = None
        
    def draw(self):
        print self.name
        pass