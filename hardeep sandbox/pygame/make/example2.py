from hmake import *
from media import *
from random import randint

app = hMain('Test')
app.start()

def event_mouse_left_click(obj, e):
    c = e.pos
    w = obj.look.w
    h = obj.look.h
    x = c[0] - (w / 2)
    y = c[1] - (h / 2)
    
    obj.set_pos((x,y))
    obj.look.set_color((randint(0, 255), randint(0, 255), randint(0, 255)))

obj = hObj('MoveRect')
obj.look = hShape.rectangle(100, 200, blue)
obj.set_pos(H_WIN_CENTER)
obj.add_event(H_EVENT_MOUSE_DOWN, event_mouse_left_click)

app.add_obj(obj)