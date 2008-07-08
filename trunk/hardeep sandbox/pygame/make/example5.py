from hmake import *
from media import *
import random

class Game(hMain):
    def __init__(self):
        hMain.__init__(self, 'Example 5 :: Gravity v2')
        self.start_physics = True
        
    def init_physics(self):
        self.set_gravity(0.0, 100.0)
        self.add_obj(ThrowableBall())
        self.add_obj(StaticBall())
        
class StaticBall(hObj):
    
    class StaticBallLook(hShape.circle):
        def get_mass(self):
            return 50000
    
    def __init__(self):
        hObj.__init__(self, 'Floor')
        
        self.set_visual_data()
        self.set_physics = True
        
        self.add_event(H_EVENT_INIT_PHYSICS, self.event_init_physics)
        
    def event_init_physics(self, obj, e):
        self.link = pymunk.Body(pymunk.inf, pymunk.inf)
        self.link.position = Vec2d(H_WIN_CENTER_COORDS[0], H_WIN_CENTER_COORDS[1]+200)
        self.join = pymunk.PinJoint(self.body, self.link, Vec2d(0,0), Vec2d(0,0))
        self.physical_space.add(self.join)
        
    def set_visual_data(self):
        self.look = StaticBall.StaticBallLook(100, red)
        self.set_pos((H_WIN_CENTER_COORDS[0], H_WIN_CENTER_COORDS[1]+200))
        
class ThrowableBall(hObj):
    def __init__(self):
        hObj.__init__(self, 'ThrowableBall')
        
        self.set_visual_data()
        self.set_physics = True
        
        self.add_event(H_EVENT_MOUSE_DOWN, self.event_mouse_down)
        
    def event_mouse_down(self, obj, e):
        factor = 100
        
        x,y = self.pos
        m_x, m_y = e.pos
        
        f_x = (H_WIN_WIDTH - m_x - x) * factor
        f_y = (H_WIN_HEIGHT - m_y - y) * factor
        
        self.add_force(f_x, f_y) # Treated as a vector (+-x, +-y)
        
    def set_visual_data(self):
        self.look = hShape.circle(random.randint(50,100), white)
        self.set_pos(H_WIN_CENTER)
        
g = Game()
g.start()