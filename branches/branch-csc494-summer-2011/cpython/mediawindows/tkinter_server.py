import Tkinter as tk

from twisted.internet import tksupport, reactor
from twisted.internet.protocol import Factory
from twisted.protocols import amp

import itertools

import mediawindows
from mediawindows import exceptions
from mediawindows.amp import (
    StartInspect, StopInspect, UpdateInspect, PollInspect)
from mediawindows import tkinter_gui as gui


class GooeyServer(amp.AMP):
    def __init__(self, *args, **kwargs):
        amp.AMP.__init__(self, *args, **kwargs)
        # no super(): AMP is a new-style class but doesn't use super().
        
        self._inspector_map = {}
    
    @StartInspect.responder
    def start_inspect(self, img):
        inspector = gui.PictureInspector(img)
        inspector_id = new_id()
        # note: references must be deleted to get rid of leaks
        self._inspector_map[inspector_id] = inspector
        inspector.protocol(
            "WM_DELETE_WINDOW",
            self.inspector_onexit(inspector_id, inspector))
        
        return dict(inspector_id=inspector_id)
    
    def inspector_onexit(self, inspector_id, inspector):
        """Return a callback for WM_DELETE_WINDOW
        
        this callback is responsible for removing the inspector from the
        live inspector mapping.
        """
        def callback():
            del self._inspector_map[inspector_id]
            inspector.destroy()
        
        return callback
        
    
    @UpdateInspect.responder
    def update_inspect(self, inspector_id, img):
        try:
            inspector = self._inspector_map[inspector_id]
        except KeyError:
            raise exceptions.WindowDoesNotExistError
        
        inspector.draw_image(img)
        return {}
    
    @PollInspect.responder
    def poll_inspect(self, inspector_id):
        return dict(is_closed=(inspector_id not in self._inspector_map))
    
    @StopInspect.responder
    def stop_inspect(self, inspector_id):
        try:
            inspector = self._inspector_map.pop(inspector_id)
        except KeyError:
            raise exceptions.WindowDoesNotExistError
        
        inspector.destroy()
        return {}

def new_id(_counter=itertools.count(1)):
    """
    Find and return a new inspector id# for use in IPC.
    
    All such numbers are positive and unique.
    
    id() was used previously, it provides insufficiently strong uniqueness
    guarantees that could, hypothetically speaking, cause bugs.
    
    Also, since all real ids will be positive, clients can feel free to use
    a nonpositive id (especially 0) as an id that will be guaranteed to not
    exist (so as to simplify implementation). This is also not a guarantee
    that id() provides.
    """
    return _counter.next()

def main():
    root = tk.Tk()
    root.withdraw()
    tksupport.install(root) # this handles the mainloop in Twisted
    
    # now we connect to the server
    factory = Factory()
    factory.protocol = GooeyServer
    reactor.listenTCP(mediawindows.amp.PORT, factory)
    
    reactor.run()

if __name__ == '__main__':
    main()
