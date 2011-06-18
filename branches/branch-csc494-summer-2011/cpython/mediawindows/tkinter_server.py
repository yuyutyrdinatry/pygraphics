import Tkinter as tk
import asyncore
import socket

import ampy.async
from ampy import ampy as amp

import itertools

import mediawindows
from mediawindows import exceptions
from mediawindows.amp import (
    StartInspect, StopInspect, UpdateInspect, PollInspect)
from mediawindows import tkinter_gui as gui

def appender(somelist):
    """
    Return an argument-taking decorator that appends its argument and decoratee
    to a list
    
        >>> L = []
        >>> a = appender(L)
        >>> @a(1)
        ... def foo(): pass
        >>> L == [(1, foo)]
        True
    
    """
    def metadecorator(arg):
        def decorator(f):
            somelist.append((arg, f))
            
            return f
        return decorator
    return metadecorator

class ProtocolBackend(object):
    """
    Protocol backends have a list of (Command, responder) pairs as their
    responder attribute. register_against() registers their responders
    against a specific AMP_Protocol instance.
    
    The usual pattern for defining a backend is:
    
        class NewProtocol(ProtocolBackend):
            responders = []
            responder = appender(responder)
            
            @responder(MyCommand)
            def my_command(self, arg1, arg2):
                # do command stuff
                # ...
                return response_dict
            
            # ...
            
    """
    def register_against(self, server):
        for command, responder_func in self.responders:
            responder_method = responder_func.__get__(self, type(self))
            server.registerResponder(command, responder_method)

class InspectorServerProtocol(ProtocolBackend):
    """
    This is a protocol backend (set of responders) the Amp protocol will 
    use for handling inspector commands.
    
    Call register_against() on an amp protocol to register its logic.
    """
    responders = []
    responder = appender(responders)
    
    def __init__(self):
        self._inspector_map = {}
    
    @responder(StartInspect)
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
    
    @responder(UpdateInspect)
    def update_inspect(self, inspector_id, img):
        try:
            inspector = self._inspector_map[inspector_id]
        except KeyError:
            raise exceptions.WindowDoesNotExistError
        
        inspector.draw_image(img)
        return {}
    
    @responder(PollInspect)
    def poll_inspect(self, inspector_id):
        return dict(is_closed=(inspector_id not in self._inspector_map))
    
    @responder(StopInspect)
    def stop_inspect(self, inspector_id):
        try:
            inspector = self._inspector_map.pop(inspector_id)
        except KeyError:
            raise exceptions.WindowDoesNotExistError
        
        inspector.destroy()
        return {}

class AskServerProtocol(ProtocolBackend):
    """
    This is a protocol backend (set of responders) the Amp protocol will 
    use for handling the ask* functions
    
    Call register_against() on an amp protocol to register its logic.
    """
    responders = []
    responder = appender(responders)

class GooeyServer(ampy.async.AMP_Server):
    built_protocol = False
    def buildProtocol(self, conn, addr):
        
        protocol_backend = InspectorServerProtocol()
        protocol = ampy.async.AMP_Protocol(conn, addr)
        protocol_backend.register_against(protocol)
        self.singleton_client = protocol
        
        self.close() # no more connections will be accepted
        # TODO: RACE CONDITION
        #       If another process tries to connect before here, they might
        #       succeed!
        return protocol

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

def listen_and_tk(server, root):
    """Run both the asyncore loop and the Tkinter loop.
    
    Inspiration taken from these sources, which may be returned to if this
    code is wrong:
    
    - http://twistedmatrix.com/trac/browser/trunk/twisted/internet/tksupport.py
    - http://mail.python.org/pipermail/chicago/2005-November/000099.html
    - https://github.com/Supervisor/supervisor/blob/master/supervisor/medusa/docs/tkinter.txt
    
    """
    while server.accepting or server.singleton_client.connected:     
        asyncore.loop(
            timeout=0.01, # block for that many seconds
            count=1, # do one iteration of select/poll
            ) 
        root.update()

def main():
    root = tk.Tk()
    root.withdraw()
    
    server = GooeyServer(mediawindows.amp.PORT) # automatically registered.
    server.start_listening()
    
    listen_and_tk(server, root)

if __name__ == '__main__':
    main()
