from hmake import *
from media import *

app = hMain('Test')
app.start()

def event_mouse_left_click(obj, e):
    obj.set_pos(e.pos)

obj = hObj('MoveRect')
obj.look = hShape.circle(100, green)
obj.set_pos(H_WIN_CENTER)
obj.add_event(H_EVENT_MOUSE_DOWN, event_mouse_left_click)

app.add_obj(obj)