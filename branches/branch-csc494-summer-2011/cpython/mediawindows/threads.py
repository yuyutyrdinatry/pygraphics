import sys
import threading
import subprocess
import atexit

from twisted.internet import reactor, defer
from twisted.internet.protocol import Factory
from twisted.internet.threads import blockingCallFromThread

from mediawindows import amp

class MediawindowsTwistedThread(object):
    """This (singleton) class represents the Twisted thread.
    
    All the public methods are meant to be called from the non-twisted thread.
    The reactor is accessible via the ``reactor`` attribute, and the
    factory is available through the ``factory`` attribute. The (only)
    AMP protocol instance is accessible through ``factory.protocol_singleton``.
    
    When writing code that does stuff with Twisted, it must be done in the
    Twisted thread, using e.g. blockingCallFromThread.
    
    See:
    
    http://twistedmatrix.com/documents/current/core/howto/threading.html
    
    """
    
    def __init__(self, reactor):
        """Initialize the mediawindows thread.
        
        Also initialize the mediawindows subprocess.
        
        This will create a new thread that runs Twisted, and an AMP server,
        and a subprocess that connects to that server.
        
        """
        ##print "Current version of Tk:"
        ##print tk.Tk().tk.call('tk', 'windowingsystem')
        self.reactor = reactor
        
        # Fire up the separate networking thread
        # NB: args=(False,) is for installSignalHandlers=False
        #     This is an undocumented parameter to Twisted which installs signal
        #     handlers when the thread is started. As it happens, signals and
        #     threads don't mix, so this has to be turned off.
        #
        #     Yes, Twisted works fine even so. Do not be alarmed!
        self.thread = threading.Thread(target=reactor.run, args=(False,))
        self.thread.daemon = True
        
        self.thread.start()
        
        blockingCallFromThread(reactor, self._twisted_thread_init)
    
    def _twisted_thread_init(self):
        """
        Initialize everything that should probably be initialized inside the
        Twisted thread (for safety's sake)
        """
        self.factory = Factory()
        self.factory.protocol = amp.GooeyHub
        self.factory.deferred_singleton = defer.Deferred()
        
        self.reactor.listenTCP(amp.PORT, self.factory)
        self.proc = subprocess.Popen(
            [sys.executable, '-m', 'pygraphics.mediawindows.tkinter_client'])
        
        # Kill the thread at exit
        atexit.register(self.shutdown)
        
        # this deferred is fired when the protocol_singleton attribute is set.
        # since this is executed in a blockingCallFromThread in __init__,
        # __init__ won't return until there is a protocol singleton (i.e. until
        # the subprocess connects)
        return self.factory.deferred_singleton
    
    def shutdown(self):
        """Shut down the mediawindows thread and subprocess
        
        This is meant to be called from another thread."""
        blockingCallFromThread(self.reactor, self.proc.terminate)
        blockingCallFromThread(self.reactor, reactor.stop)
        self.thread.join()

def init_mediawindows(*args, **kwargs):
    import mediawindows # NOT from pygraphics import mediawindows. Guess why!
    global _THREAD_SINGLETON
    mediawindows._THREAD_RUNNING = True # this is so silly.
    _THREAD_SINGLETON = MediawindowsTwistedThread(reactor, *args, **kwargs)
    # 'cause, I mean, globals, right?

# This stuff uses the global _THREAD_SINGLETON object

def threaded_callRemote(*args, **kwargs):
    """callRemote using _THREAD_SINGLETON.factory.protocol_singleton
    
    This is a convenience function, because all that typing is annoying.
    
    """
    reactor = _THREAD_SINGLETON.reactor
    protocol = _THREAD_SINGLETON.factory.protocol_singleton
    
    return blockingCallFromThread(reactor, protocol.callRemote, *args, **kwargs)
