import threading
import subprocess

from twisted.protocols import amp
from twisted.internet import reactor
from twisted.internet.threads import blockingCallFromThread

# oh jeez we need a unique port on windows. On *nix we could use domain sockets
PORT = 31337

####################------------------------------------------------------------
## The actual Twisted thread stuff
####################------------------------------------------------------------

class MediawindowsTwistedThread(object):
    def __init__(self):
        """Initialize the mediawindows thread.
        
        Also initialize the mediawindows subprocess."""
        
        ##print "Current version of Tk:"
        ##print tk.Tk().tk.call('tk', 'windowingsystem') 
        
        # Fire up the separate networking thread
        self.thread = threading.Thread(target=self.run)
        
        # Kill the thread at exit
        atexit.register(self.shutdown)
        
        self.thread.run()
    
    def run(self):
        from twisted.internet import reactor
        from twisted.internet.protocol import Factory
        pf = Factory()
        pf.protocol = GooeyHub
        
        reactor.listenTCP(PORT, pf)
        self.proc = subprocess.Popen(
            [sys.executable, 'pygraphics.twisted_mediawindows_gui'])
        reactor.run()
    
    def shutdown(self):
        """Shut down the mediawindows thread and subprocess"""
        # RACE CONDITION: what if shutdown happens before run() gets to where
        #                 it creates self.proc? or reactor.run()?
        #                 (I care about this very little, but it's always worth
        #                  documenting)
        blockingCallFromThread(reactor, self.proc.terminate)
        blockingCallFromThread(reactor, reactor.stop)
        self.thread.join()

def init_mediawindows(*args, **kwargs):
    global _THREAD_SINGLETON
    _THREAD_SINGLETON = MediawindowsTwistedThread(*args, **kwargs)
    # 'cause, I mean, globals, right?
    
####################------------------------------------------------------------
## AMP Protocol
####################------------------------------------------------------------

class StartInspect(amp.Command):
    arguments = [
        ('img_data', amp.String()),
        ('img_width', amp.Integer()),
        ('img_height', amp.Integer()),
        ('img_mode', amp.String())]
    response = [('inspector_id', amp.Integer())]

class StopInspect(amp.Command):
    arguments = [
        ('inspector_id', amp.Integer())]
    response = []

class GooeyHub(amp.AMP):
    pass
