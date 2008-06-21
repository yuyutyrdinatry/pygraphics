#!/usr/bin/env python
# Hmmmm it might be possible to create the show window using pyglet?? :o

import sys

from pyglet.gl import *
from pyglet import window
from pyglet import image

import threading

class ShowWrapperThread(threading.Thread):
    '''Wraps the ShowOMatic into it's own thread.'''    
        
    def run(self):
        #PIL -> Image
        #http://www.pyglet.org/doc/programming_guide/loading_an_image.html
        self.filename = filename = "test.png"
    
        self.w = w = window.Window(visible=False, resizable=True)
        self.img = img = image.load(filename).texture
    
        checks = image.create(32, 32, image.CheckerImagePattern())
        self.background = background = image.TileableTexture.create_for_image(checks)
    
        w.width = img.width
        w.height = img.height
        w.set_visible()
    
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  
        
        while not w.has_exit:
            w.dispatch_events()
            
            background.blit_tiled(0, 0, 0, w.width, w.height)
            img.blit(0, 0, 0)
            w.flip()

#if __name__ == '__main__':
    a = ShowWrapperThread()
    a.start()