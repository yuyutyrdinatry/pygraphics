# What about a more complex example? Lets say a bouncing ball that the user
# can click on and it would push around. Complete with physics and all! 
# Scrapped the Gravity idea for now because I don't want to have to figure 
# out all the Gravity math again as I'm not sure how to use PyMunk to do 
# gravity per object yet. At least not how it would be required.
#
# Once complete, this would ideally create a white screen with a black ball
# that the user could click on. Depending on where the user clicked and how
# far from the object he clicked, it would propel the ball away in the
# opposite direction. The mass of the ball would be dependant on its size
# which is random between [50, 200] inclusive. Note that it would be
# compatible with PyGraphics colors and such as well! Ideally, you could use
# both together to generate graphics for your games on the fly for example.
# And PyGraphics sound could be used for sound as well, which is already
# PyGame based anyways.

# Let's make all this work!
from hmake import *
from media import *
import random

class Game(hMain):
    def __init__(self):
        hMain.__init__(self, 'Gravity')
        
        self.add_obj(ThrowableBall())
        self.set_gravity(0.0, -900.0)
        
class ThrowableBall(hObj):
    def __init__(self):
        hObj.__init__('ThrowableBall')
        self._set_visual_properties()
        self._set_physical_properties()
        
        # Makes it a physical rigid-body object. It will no longer be able to
        # be controlled directly, all movement must be done through inertia
        # modifications or by linking to another object! For example, the mouse
        self.set_physics(True, H_PHYS_RIGID)
        
        self.add_event('mouse_left_click', self.event_mouse_left_click)
        
    def event_mouse_left_click(self, e):
        x,y = self.pos
        m_x, m_y = e.mouse_pos
        
        self.set_inertia(m_x - x, m_y - y)
        
    def _set_visual_properties(self):
        hObj._set_visual_properties(self)
        
        self.color = media.black
        self.radius = random.randint(50,200)
        self.look = hShape.circle(radius, color)
        self.inital_pos = H_WIN_CENTER
        
    def _set_physical_properties(self):
        hObj._set_physical_properties(self)
        
        self.mass = self.radius
        
g = Game()
g.start()