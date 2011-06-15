import socket
import errno
import time
import os
import sys
import subprocess
import atexit

from ampy import ampy as amp

import mediawindows as mw

class MediawindowsAmpyConnection(object):
    """This (singleton) class represents the connection to the client.
    
    """
    
    def __init__(self):
        """Initialize the mediawindows subprocess and connection.
        
        This will create a subprocess (an AMP server), and connect to it.
        
        """
        ##print "Current version of Tk:"
        ##print tk.Tk().tk.call('tk', 'windowingsystem')
        self.proc, self.proxy = self.create_connection()
        
        # Kill the process at exit
        atexit.register(self.shutdown)
    
    def create_connection(self):
        """Create a subprocess, return it and a connection to it.
        
        Doing this without incurring race conditions is hard.
        
        """
        # TODO: add auto-incrementing ports.
        # idea: check for the subprocess dying, restart if it does.
        #       continue until we have a connection.
        #       Make the server only accept one connection to counter-act
        #       multiple ports.
        #
        #       OR: if there's an existing process, connect to it anyway?
        #       background processes work fine...
        #       Actually, no they don't. There are blocking calls involved.
        #       (in particular in the ask* functions).
        proc = subprocess.Popen(
                [sys.executable, '-m', get_submodule_name('tkinter_server'),
                 'server'], # last element is hack to get stuff working
                )
        proxy = amp.Proxy('127.0.0.1', mw.amp.PORT, socketTimeout=None)
        while 1:
            if proc.poll() is not None:
                raise RuntimeError("Subprocess exited")
            try:
                proxy.connect()
            except socket.error, e:
                if e.errno not in [errno.ECONNREFUSED, errno.ETIMEDOUT]:
                    raise
                time.sleep(.1) # retry if one of the above
            else:
                break
        
        return proc, proxy
    
    def shutdown(self):
        """Shut down the mediawindows subprocess"""
        self.proc.terminate()

def get_submodule_name(submodule):
    return 'mediawindows.%s' % (submodule,) # eech seems risky
    # TODO: turn this into import ... .__name__, like it was before.
    # imports don't work atm because the server is in Twisted, not ampy.
    # That is slated to change, of course.

def callRemote(*args, **kwargs):
    return _CONNECTION_SINGLETON.proxy.callRemote(*args, **kwargs)

def init_mediawindows(*args, **kwargs):
    global _CONNECTION_SINGLETON
    import mediawindows
    if not mediawindows._MEDIAWINDOWS_INITIALIZED:
        mediawindows._MEDIAWINDOWS_INITIALIZED = True
        _CONNECTION_SINGLETON = MediawindowsAmpyConnection(*args, **kwargs)
        # 'cause, I mean, globals, right?
    
    
