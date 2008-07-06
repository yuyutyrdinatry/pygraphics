import os, sys
import wx
import thread

global pygame

class SDLThread:
    def __init__(self, screen):
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
        # This is the actual game loop!
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
        parent.thread.Start()

    def __del__(self):
        self.parent.Stop()

class SDLFrame(wx.Frame):
    def __init__(self, parent, ID, strTitle, tplSize):
        wx.Frame.__init__(self, parent, ID, strTitle, size=tplSize)
        self.pnlSDL = SDLPanel(self, -1, tplSize)