from hmake import *
from media import *
from random import randint

app = hMain('Example 2')
app.start()

def event_mouse_left_click(obj, e):
    # e.pos is a tuple which is the mouse click location (x, y)
    # obj.look.w is width of the object, look.h is height
    #
    # and so the below code lets us calculate the center of the rectangle and
    # position it accordingly
    obj.set_pos((e.pos[0] - (obj.look.w / 2), 
                 e.pos[1] - (obj.look.h / 2)))
    obj.look.set_color((randint(0, 255), randint(0, 255), randint(0, 255)))

obj = hObj('MoveRect')
obj.look = hShape.rectangle(100, 200, blue)
obj.set_pos(H_WIN_CENTER)
obj.add_event(H_EVENT_MOUSE_DOWN, event_mouse_left_click)

app.add_obj(obj)