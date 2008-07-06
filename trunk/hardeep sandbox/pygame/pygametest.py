# You know, I keep thinking it'd be really cool to have a very simple game-
# maker sort of class that could allow people to relatively easily put together
# simple games. Indeed. It would be quite cool.

import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class hMain(object):
    '''The main game object.'''
    
    def __init__(self, *args, **kwargs):
        pygame.init()
        self.screen = pygame.display.set_mode((468, 60))
        pygame.display.set_caption('Monkey Fever')
        pygame.mouse.set_visible(0)
        
def test(*args, **kwargs):
    print args, kwargs