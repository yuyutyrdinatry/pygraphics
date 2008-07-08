from hmake import *
from media import *
import random
from random import randint

class Game(hMain):
    def __init__(self):
        hMain.__init__(self, 'Example 5 :: Gravity v2 :: LMB - Force | RMB - Reset')
        self.start_physics = True
        
    def _make_statball(self, x, y):
        return StaticBall(x, y, (randint(0,255), randint(0,255), randint(0,255)))
        
    def init_physics(self):
        self.set_gravity(0.0, 900.0)
        self.add_obj(ThrowableBall())
        
        x = 16
        y = H_WIN_CENTER_COORDS[1] + 150
        for i in xrange(0, 18):
            x += 32
            self.add_obj(self._make_statball(x, y))
            
        y = H_WIN_CENTER_COORDS[1] + 150
        for i in xrange(0, 10):
            y -= 32
            self.add_obj(self._make_statball(x, y))
            
        x = 16
        y = H_WIN_CENTER_COORDS[1] + 150
        for i in xrange(0, 10):
            y -= 32
            self.add_obj(self._make_statball(x, y))
        
        x = 16
        y -= 32
        for i in xrange(0, 18):
            x += 32
            self.add_obj(self._make_statball(x, y))
        
class StaticBall(hObj):
    
    def __init__(self, x, y, col):
        hObj.__init__(self, 'Floor')
        
        self.set_visual_data(col)
        self.set_physics = True
        
        self.set_pos((x, y))
        
        self.add_event(H_EVENT_INIT_PHYSICS, self.event_init_physics)
        
    def event_init_physics(self, obj, e):
        self.link = pymunk.Body(pymunk.inf, pymunk.inf)
        self.link.position = Vec2d(self.pos[0], self.pos[1])
        
        self.join = pymunk.PinJoint(self.body, self.link, Vec2d(0,0), Vec2d(0,10))
        self.physical_shape.friction = 0.0
        self.physical_shape.elasticity = 1.0
        
        self.physical_space.add(self.join)
        
    def set_visual_data(self, col):
        self.look = hShape.circle(10, col)
        
class ThrowableBall(hObj):
    def __init__(self):
        hObj.__init__(self, 'ThrowableBall')
        
        self.set_visual_data()
        self.set_physics = True
        
        self.add_event(H_EVENT_MOUSE_DOWN, self.event_mouse_down)
        self.add_event(H_EVENT_INIT_PHYSICS, self.event_init_physics)
        
    def event_init_physics(self, obj, e):
        self.physical_shape.friction = 0.0
        self.physical_shape.elasticity = 1.0
        
    def event_mouse_down(self, obj, e):
        if e.button == 3:
            self.reset_forces()
        else:
            factor = 10
            
            x,y = self.pos
            m_x, m_y = e.pos
            
            f_x = (H_WIN_WIDTH - m_x - x) * factor
            f_y = (H_WIN_HEIGHT - m_y - y) * factor
            
            self.add_impulse(f_x, f_y, (f_x * -1, f_y * -1)) # Treated as a vector (+-x, +-y)
        
    def set_visual_data(self):
        self.look = hShape.circle(50, white)
        self.set_pos(H_WIN_CENTER)
        
g = Game()
g.start()