#!/usr/bin/env python
# Hmmmm it might be possible to create the show window using pyglet?? :o

import sys

from pyglet.gl import *
from pyglet import window
from pyglet import image
from Image import FLIP_TOP_BOTTOM

import threading

import media as m

class ShowWrapperThread(threading.Thread):
    '''Wraps the ShowOMatic into it's own thread.'''
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.img = None
        self.w = None
        
    def _create_and_init_window(self):
        self.w = window.Window(visible=False, resizable=False)
    
        checks = image.create(32, 32, image.CheckerImagePattern())
        self.background = image.TileableTexture.create_for_image(checks)
    
        self.w.width = 1
        self.w.height = 1
        self.w.set_visible()
    
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
    def _main_loop(self):
        while not self.w.has_exit:
            self.w.dispatch_events()
            
            self.background.blit_tiled(0, 0, 0, self.w.width, self.w.height)
            if ( self.img is not None ):
                self.img.blit(0, 0, 0)
            
            self.w.flip()
    
    def load_image(self, p):
        if ( self.w is not None ):
            self.pic = p
            self.img = image_to_psurf(p.get_image())
            self.w.width = self.img.width
            self.w.height = self.img.height    
        else:
            while ( self.w is None ):
                True # Wait until the window is active
            self.load_image(p)
        
    def run(self):
        self._create_and_init_window()
        self._main_loop()
            
def image_to_psurf(im):
    im = im.transpose(FLIP_TOP_BOTTOM)
    return image.ImageData(im.size[0], im.size[1], "RGB", im.tostring())

if __name__ == '__main__':
    a = ShowWrapperThread()
    a.start()
    
    p1 = m.create_picture(900,200,m.black)
    p2 = m.create_picture(300,100,m.red)
    p3 = m.create_picture(150,150,m.green)
    
    a.load_image(p1)
    raw_input('press enter to load next image...')
    
    a.load_image(p2)
    raw_input('press enter to load next image...')
    
    a.load_image(p3)
    raw_input('press enter to exit...')