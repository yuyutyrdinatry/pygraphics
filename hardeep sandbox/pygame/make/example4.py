from hmake import *
from media import *
from random import randint

app = hMain('Example 4 :: LMB to add object')
app.start()

def event_mouse_move(obj, e):
    obj.set_pos(e.pos)
    
def event_mouse_down(obj, e):
    global app
    app.add_obj(_create_new_obj(e.pos))

def _create_new_obj(pos):
    obj = hObj('new_obj_' + str(randint(0,100000)))
    obj.look = hShape.circle(10, (randint(0, 255), 
                                  randint(0, 255), 
                                  randint(0, 255)))
    obj.set_pos(pos)
    return obj

obj = hObj('MoveRect')
obj.look = hShape.circle(15, yellow, width=4)
obj.set_pos(H_WIN_CENTER)
obj.add_event(H_EVENT_MOUSE_MOVE, event_mouse_move)
obj.add_event(H_EVENT_MOUSE_DOWN, event_mouse_down)

app.add_obj(obj, 100)