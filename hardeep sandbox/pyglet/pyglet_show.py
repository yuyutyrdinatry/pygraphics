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
    
    def load_image(self, p):
        self.pic = p
        self.img = image_to_psurf(p.get_image())
        self.w.width = self.img.width
        self.w.height = self.img.height    
        
    def run(self):
        self.w = window.Window(visible=False, resizable=False)
    
        checks = image.create(32, 32, image.CheckerImagePattern())
        self.background = background = image.TileableTexture.create_for_image(checks)
    
        self.w.width = 1
        self.w.height = 1
        self.w.set_visible()
    
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  
        
        while not self.w.has_exit:
            self.w.dispatch_events()
            
            background.blit_tiled(0, 0, 0, self.w.width, self.w.height)
            if ( self.img is not None ):
                self.img.blit(0, 0, 0)
            
            self.w.flip()
            
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