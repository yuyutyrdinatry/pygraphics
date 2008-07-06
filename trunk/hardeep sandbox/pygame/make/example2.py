from hmake import *
from media import *

app = hMain('Test')
app.start()

def event_mouse_left_click(self, e):
    e.obj.set_xy(event.mouse.x, event.mouse.y)

obj = hObj('MoveRect')
obj.look = 
obj.look = hShape.circle(100, 100, red)
obj.initial_pos = H_WIN_CENTER
obj.add_event('mouse_left_click', move_obj)

app.add_obj(obj)
# --------------------------------------------------------------------------
# Now THAT would be sick