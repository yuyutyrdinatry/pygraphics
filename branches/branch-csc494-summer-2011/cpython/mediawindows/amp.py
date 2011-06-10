import sys
import threading
import subprocess
import atexit
from cStringIO import StringIO
from itertools import count

from twisted.protocols import amp
from twisted.internet import reactor, defer
from twisted.internet.threads import blockingCallFromThread
from twisted.internet.protocol import Factory

import Image
import zope.interface

from mediawindows import gui, exceptions

# oh jeez we need a unique port on windows. On *nix we could use domain sockets
PORT = 31337

####################------------------------------------------------------------
## The actual Twisted thread stuff
####################------------------------------------------------------------

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
        self.factory.protocol = GooeyHub
        self.factory.deferred_singleton = defer.Deferred()
        
        self.reactor.listenTCP(PORT, self.factory)
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

####################------------------------------------------------------------
## AMP Protocol / related things
####################------------------------------------------------------------

# BigString is stolen from the AMP docs. Turns out you can't pass
# things larger than 64k...
# http://amp-protocol.net/Types/BigString

CHUNK_MAX = 0xffff
class BigString(amp.Argument):
    def fromBox(self, name, strings, objects, proto):
        value = StringIO()
        value.write(strings.get(name))
        for counter in count(2):
            chunk = strings.get("%s.%d" % (name, counter))
            if chunk is None:
                break
            value.write(chunk)
        objects[name] = self.buildvalue(value.getvalue())
 
    def buildvalue(self, value):
        return value
 
    def toBox(self, name, strings, objects, proto):
        value = StringIO(self.fromvalue(objects[name]))
        firstChunk = value.read(CHUNK_MAX)
        strings[name] = firstChunk
        counter = 2
        while True:
            nextChunk = value.read(CHUNK_MAX)
            if not nextChunk:
                break
            strings["%s.%d" % (name, counter)] = nextChunk
            counter += 1
 
    def fromvalue(self, value):
        return value
 
class BigUnicode(BigString):
    def buildvalue(self, value):
        return value.decode('utf-8')
    
    def fromvalue(self, value):
        return value.encode('utf-8')


class PILImage(object):
    """
    This is an AMP argument converter that transforms PIL Image objects to and
    from four string key-value pairs in the AMP message.
    
    keys are of the form <name>.<subkey>, and the subkeys are as follows:
        
        data
            the binary blob containing the image data
        width
            the integer width
        height
            the integer height
        mode
            the string image mode
    
    """
    # I'm a bit iffy about creating new keys... in theory they could conflict
    # with other keys. The alternative is packing this with json or something,
    # but that's slow and I'm lazy.
    zope.interface.implements(amp.IArgumentType)
    
    bigstring = BigString()
    
    def toBox(self, name, strings, objects, proto):
        img = objects[name]
        w, h = img.size
        strings.update({
            '%s.width' % name: str(w),
            '%s.height' % name: str(h),
            '%s.mode' % name: img.mode})
        
        dataname = "%s.data" % name
        self.bigstring.toBox(
            dataname, strings, {dataname:img.tostring()}, proto)
    
    def fromBox(self, name, strings, objects, proto):
        dataname = "%s.data" % name
        tempd = {}
        self.bigstring.fromBox(dataname, strings, tempd, proto)
        
        objects[name] = Image.fromstring(
            strings['%s.mode' % name],
            (
                int(strings['%s.width' % name]),
                int(strings['%s.height' % name])),
            tempd['%s.data' % name])


class StartInspect(amp.Command):
    arguments = [
        ('img', PILImage())]
    response = [('inspector_id', amp.Integer())]

class UpdateInspect(amp.Command):
    arguments = [
        ('inspector_id', amp.Integer()),
        ('img', PILImage())]
    response = []
    errors = {exceptions.WindowDoesNotExistError: 'WINDOW_DOES_NOT_EXIST'}

class StopInspect(amp.Command):
    arguments = [
        ('inspector_id', amp.Integer())]
    response = []
    errors = {exceptions.WindowDoesNotExistError: 'WINDOW_DOES_NOT_EXIST'}

class PollInspect(amp.Command):
    arguments = [
        ('inspector_id', amp.Integer())]
    response = [('is_closed', amp.Boolean())]

class GooeyHub(amp.AMP):
    def connectionMade(self):
        """Here we will set the global connected subprocess.
        
        If, in the future, multiple subprocesses will be supported, this must
        be modified to support that. Currently the server only accepts one
        client.
        
        """
        amp.AMP.connectionMade(self)
        
        self.factory.protocol_singleton = self
        self.factory.deferred_singleton.callback(self)
