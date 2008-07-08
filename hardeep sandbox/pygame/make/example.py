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
        hMain.__init__(self, 'Example 1 :: Gravity')
        
        # Note that you must set start_physics to True and also set the data for
        # gravity BEFORE adding objects that will use physics. If you are adding
        # initial objects which will be included in the physics simulation,
        # place them in the init_physics method! You may also define the Gravity
        # there.
        self.start_physics = True
        
    def init_physics(self):
        self.set_gravity(0.0, 100.0)
        self.add_obj(ThrowableBall())
        
class Floor(hObj):
    def __init__(self):
        hObj.__init__(self, 'Floor')
        
        self.set_visual_data()
        self.set_physics = True
        
class ThrowableBall(hObj):
    def __init__(self):
        hObj.__init__(self, 'ThrowableBall')
        
        self.set_visual_data()
        
        # Makes it a physical rigid-body object. It will no longer be able to
        # be controlled directly, all movement must be done through inertia
        # modifications or by linking to another object! For example, the mouse
        # will have an invisible object following it at all times. Objects can
        # then be linked to it in a variety of ways. Note that it MUST be called
        # after the look of the object has been defined! Also initial position
        # MUST BE SET!
        self.set_physics = True
        
        self.add_event(H_EVENT_MOUSE_DOWN, self.event_mouse_down)
        
    def event_mouse_down(self, obj, e):
        self.body.position = e.pos[0], e.pos[1]
#        factor = 0.1
#        
#        x,y = self.pos
#        m_x, m_y = e.pos
#        
#        f_x = (H_WIN_WIDTH - m_x - x) * factor
#        f_y = (H_WIN_HEIGHT - m_y - y) * factor
#        self.add_force(f_x, f_y) # Treated as a vector (+-x, +-y)
        
    def set_visual_data(self):
        self.look = hShape.circle(random.randint(50,100), white)
        self.set_pos(H_WIN_CENTER)
        
g = Game()
g.start()