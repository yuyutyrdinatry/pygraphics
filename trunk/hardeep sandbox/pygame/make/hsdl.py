import os, sys
import wx
import threading

global pygame

class SDLThread(threading.Thread):
    def __init__(self, screen):
        threading.Thread.__init__(self)
        
        self.m_bKeepGoing = False
        self.screen = screen
        self.color = (255,0,0)
        self.rect = (10,10,100,100)
        
    def add_obj(self, o):
        self.objects.append(o)

    def run(self):
        self.m_bKeepGoing = True
        while self.m_bKeepGoing:
            self._main_loop()
            pygame.display.flip()

    def stop(self):
        self.m_bKeepGoing = False
        
    def _main_loop(self):
        e = pygame.event.poll()
        
        if e.type == pygame.MOUSEBUTTONDOWN:
            self.color = (255,0,128)
            self.rect = (e.pos[0], e.pos[1], 100, 100)
            print e.pos
            
        for o in self.objects:
            o.draw()
            
        self.screen.fill((0,0,0))
        self.screen.fill(self.color,self.rect)

class SDLPanel(wx.Panel):
    def __init__(self,parent,ID,tplSize):
        '''Init pygame display into the Frame as a Panel.'''
        global pygame
        
        wx.Panel.__init__(self, parent, ID, size=tplSize)
        self.Fit()
        
        os.environ['SDL_WINDOWID'] = str(self.GetHandle())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        
        # this has to happen after setting the environment variables.
        import pygame
        
        pygame.display.init()
        self.window = pygame.display.set_mode(tplSize)
        
        self.parent = parent
        parent.thread = SDLThread(self.window)
        parent.thread.start()

    def __del__(self):
        self.parent.stop()

class SDLFrame(wx.Frame):
    def __init__(self, parent, ID, strTitle, tplSize):
        wx.Frame.__init__(self, parent, ID, strTitle, size=tplSize)
        self.panel = SDLPanel(self, -1, tplSize)