# You know, I keep thinking it'd be really cool to have a very simple game-
# maker sort of class that could allow people to relatively easily put together
# simple games. Indeed. It would be quite cool.

import os, sys
import wx
import thread
from pygame.locals import *
global pygame # when we import it, let's keep its proper name!

class SDLThread:
    def __init__(self,screen):
        self.m_bKeepGoing = self.m_bRunning = False
        self.screen = screen
        self.color = (255,0,0)
        self.rect = (10,10,100,100)

    def Start(self):
        self.m_bKeepGoing = self.m_bRunning = True
        thread.start_new_thread(self.Run, ())

    def Stop(self):
        self.m_bKeepGoing = False

    def IsRunning(self):
        return self.m_bRunning

    def Run(self):
        while self.m_bKeepGoing:
            e = pygame.event.poll()
            if e.type == pygame.MOUSEBUTTONDOWN:
                self.color = (255,0,128)
                self.rect = (e.pos[0], e.pos[1], 100, 100)
                print e.pos
            self.screen.fill((0,0,0))
            self.screen.fill(self.color,self.rect)
            pygame.display.flip()
        self.m_bRunning = False;

class SDLPanel(wx.Panel):
    def __init__(self,parent,ID,tplSize):
        global pygame
        wx.Panel.__init__(self, parent, ID, size=tplSize)
        self.Fit()
        os.environ['SDL_WINDOWID'] = str(self.GetHandle())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        import pygame # this has to happen after setting the environment variables.
        pygame.display.init()
        window = pygame.display.set_mode(tplSize)
        self.thread = SDLThread(window)
        self.thread.Start()

    def __del__(self):
        self.thread.Stop()

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, strTitle, tplSize):
        wx.Frame.__init__(self, parent, ID, strTitle, size=tplSize)
        self.pnlSDL = SDLPanel(self, -1, tplSize)

app = wx.PySimpleApp()
frame = MyFrame(None, wx.ID_ANY, "SDL Frame", (640,480))
frame.Show()
app.MainLoop()