====================================
GUIs in PyGraphics: Working With AMP
====================================

What is AMP?
============

AMP_ is the *Asynchronous Messaging Protocol*, a bidirectional RPC protocol
used by PyGraphics to communicate between processes.

Why do we have multiple processes and RPC?
------------------------------------------

Part of what PyGraphics does is let the user display images to the screen,
after the user has made some changes, and continue to display the image while
the user does work.

Originally, this was done via PIL's show_ method. (And before that, through
pygame_). When this didn't work, it was replaced with a custom-built GUI window
implemented through ImageTk. 

Because images are supposed to be shown while the Python interactive interpreter
is running, a new thread would be created for Tkinter to run its event loop, and
messages would be passed to create new windows etc.

Unfortunately, threading didn't work out either. OS X 10.6 wouldn't permit
TkAqua to be initialized from the wrong thread, as documented here_.

Several solutions were attempted with running Tkinter in another thread.
During the summer of 2011, it was removed and placed in another process instead.
However, threads were kept for running IPC. Even this use of threads had to
be removed, due to a known_ dead-lock in the Python import system that would
make students' code too fragile. Currently, PyGraphics does not use threads at
all, and instead uses AMP with ampy_

.. _AMP: http://amp-protocol.net/
.. _show: http://www.pythonware.com/library/pil/handbook/image.htm#Image.show
.. _pygame: http://www.pygame.org/
.. _here: http://code.google.com/p/pygraphics/wiki/MacInstall
.. _known: http://docs.python.org/library/threading.html#importing-in-threaded-code
.. _ampy: https://launchpad.net/ampy

How PyGraphics uses AMP
-----------------------

When :py:func:`mediawindows.init_mediawindows` is called, a subprocess is
created that runs :py:mod:`mediawindows.tkinter_server`. The current process
connects to the subprocess on a constant port (:py:data:`mediawindows.amp.PORT`)
and from then on they communicate via AMP.

Any functions that require asynchronously executing code (in particular, GUI
windows) must code this as an AMP command, send it over the connection, where it
is decoded by the subprocess and executed.

Creating your own AMP command
=============================

In this tutorial, we will be implementing :py:func:`media.say`. The code
used to implement that was written as part of writing this tutorial.

The first step in creating a new function that needs to use AMP for IPC is to
figure out what that function does, of course! This function will produce a
GUI window with some text in it. So our function will take a single parameter,
"text"::

    def say(text):
        """Put some text in a GUI window and stuff.
        
        say is called with one argument, you can use it like this:
        
            >>> say("foo")
        
        and say will return right away. You can even put up multiple windows
        at once!
        """
        
        # what do we put here?
        pass

In particular, this text is the only thing that needs to be communicated to
the other process, too. The GUI process only needs to know that it is displaying
text, and what text to display. It won't communicate anything back, and it won't
raise any exceptions.

So the next, and most important step, is to define the inter-process interface.
AMP is used in a statically-typed fashion, with commands crafted with specific
arguments of specific types, so that AMP knows how to transmit them on the wire.

There are no positional arguments in an AMP command, just keyword arguments.
Similarly, AMP commands only return dictionaries. So our amp command will
take in a single keyword argument: :samp:`"text"`, and return a dict with
no keys (the empty dict, :samp:`{}`)


.. sidebar:: BigString
    
    In this case, we use BigString as the type for the value. This is because
    the size of AMP values is limited to 64k, and maybe one of our users is
    really fun and wants to see what happens when he sends his aunt's gigantic
    excel spreadsheet from work over to the say command.
    
    Realistically speaking, it doesn't matter for this. Where it *does* matter
    is when sending images, and :py:class:`mediawindows.amp.PILImage` uses 
    BigString internally so that we can send images larger than 64k.

To write all of this down, we would write the following class into 
:mod:`mediawindows.amp`::

    class Say(amp.Command):
        arguments = [
            ('text', BigString())]
        response = []

.. topic:: Static typing in AMP

    `arguments` is a list of :samp:`{key}, {AmpType}` pairs. :mod:`ampy` has a lot
    of types for representing Python values, including:

     - :py:class:`ampy.ampy.Integer`
     - :py:class:`ampy.ampy.Float`
     - :py:class:`ampy.ampy.Boolean`
     - :py:class:`ampy.ampy.String`
     - :py:class:`ampy.ampy.Unicode`

    In addition, :py:mod:`mediawindows.amp` offers the following extra AMP types:

     - :py:class:`mediawindows.amp.BigString`
     - :py:class:`mediawindows.amp.BigUnicode`
     - :py:class:`mediawindows.amp.PILImage`

    Each of these let you pass in Python values of that type and get the same
    value back on the other side of the AMP connection.

By declaring there to be an argument of name 'text' and value 
:py:class:`mediawindows.amp.BigString`, we allow :py:class:`BigString` to handle 
serialization and deserialization of the 'text' keyword argument we pass or 
receive during a :py:class:`Say` command.

A complete :py:func:`media.say`
-------------------------------

Before implementing the responder, let's implement the front-end. 
:py:mod:`media.py` will have a :py:func:`say` function that sends this AMP
command to the Tkinter process.

It would be helpful to learn how to send commands!

.. py:function mediawindows.callRemote(command, **kw)

    Given a Command class object `command`, and arbitrary keyword-arguments,
    pack those arguments into an AMP message and send them to the
    GUI subprocess.

So say should look exactly like this::

    def say(text):
        """Put some text in a GUI window and stuff.
        
        say is called with one argument, you can use it like this:
        
            >>> say("foo")
        
        and say will return right away. You can even put up multiple windows
        at once!
        """
        
        mw.callRemote(amw.mp.Say, text=text)

We would probably put this inside :py:mod:`mediawindows.proxy`, and then
have a short stub function in :py:mod:`media` that goes as follows::

    def say(text):
        """Put some text in a GUI window and stuff.
        
        say is called with one argument, you can use it like this:
        
            >>> say("foo")
        
        and say will return right away. You can even put up multiple windows
        at once!
        """
        
        return mw.say(text)

It's worth noting that :py:func:`mediawindows.say` is called, and not 
:py:func:`mediawindows.proxy.say`. While :py:mod:`mediawindows` is a package
(a module implemented using a directory with multiple submodules),
it exports an interface to other modules that makes it usable as a plain
module. No :py:mod:`mediawindows` submodule should be used in new code in 
general, especially not :py:mod:`media`, as it's read by first-year students who
are very early into their CS education.

To do this, the following line might be added to 
:py:mod:`mediawindows.__init__`::

    from .proxy import say

Making it actually work
-----------------------

Sending an AMP command is all well and good, but if we try to actually invoke
the command, we'll get an exception something like the following::

    Traceback (most recent call last):
      File "...", line 1, in <module>
      File ".../pygraphics/media.py", line 530, in say
        return mw.say(text)
      File ".../pygraphics/mediawindows/proxy.py", line 43, in say
        mw.callRemote(mw.amp.Say, text=text)
      File ".../pygraphics/mediawindows/client.py", line 62, in callRemote
        return _CONNECTION_SINGLETON.proxy.callRemote(*args, **kwargs)
      File ".../ampy/ampy.py", line 152, in callRemote
        return self._callRemote(command, True, **kw)
      File ".../ampy/ampy.py", line 200, in _callRemote
        wireResponse[ERROR_DESCRIPTION])
      File ".../ampy/ampy.py", line 230, in _raiseProxiedError
        raise AMPError(code, description)
    ampy.ampy.AMPError: ('UNHANDLED', 'No handler for command')

This is good! This exception means that the message was sent fine, it was
received by the GUI subprocess, but the GUI subprocess indicated an error back
to us: it doesn't know what to do with a :py:class:`Say` command. The
solution is to implement a handler for :py:class:`Say` inside the GUI
subprocess.

The GUI subprocess is implemented in :py:mod:`mediawindows.tkinter_server`.
This module is executed, creates an AMP server, and starts a listening socket.
When it gets its first connection (hopefully the parent process), it stops
listening for new connections, and handles AMP commands from the client.
When it is disconnected from and all its windows have been closed, it
terminates. (:py:mod:`mediawindows` will not permit the main Python process
to exit until this has happened).

Because :py:mod:`ampy` doesn't have a lot of tools for writing AMP servers
(or clients), a bit of infrastructure is provided in the form of this class:

.. autoclass:: mediawindows.tkinter_server.ProtocolBackend

To define a handler for our command, we need a new protocol backend for it,
and we need to make sure the protocol backend is registered against the actual
AMP connection when it's created.

First, we define our backend. Just so that we can be sure this works,
instead of opening up a new GUI window, we'll use the print statement::

    class SayServerProtocol(ProtocolBackend):
        """
        This is a protocol backend (set of responders) the Amp protocol will 
        use for handling the say function.
        
        Call register_against() on an amp protocol to register its logic.
        """
        responders = []
        responder = appender(responders)
        
        @responder(Say)
        def say(self, text):
            print text
            return {}

There are a couple of important things to note.

#. SayProtocol has a class variable `responders` and `responder`.
   
   `responders` is used by 
   `:py:meth:`mediawindows.tkinter_server.ProtocolBackend.registerAgainst`
   to register command handlers against commands.
   
   `responder` is a decorator only used inside the class body, which appends
   to `responders` when called appropriately.
   
   When you want to define a new responder, you can decorate it with
   @responder(CommandClass)

#. say returns {}

   Every responder is required to return a value, no matter if it's used by the
   other side or not. The value is always a dictionary. In the case of
   :py:class:`Say`, the dictionary should be empty, because there are no
   keys defined in ``Say.response``.

By itself, :py:class:`SayServerProtocol` doesn't do anything. It still needs
to be registered against the actual connection, so the following lines need
to be added to 
:py:meth:`mediawindows.tkinter_server.GooeyServer.buildProtocol`::

        self._say_prot = SayServerProtocol()
        self._say_prot.register_against(protocol)

So now what happens when we run try to use this?

    >>> import media
    >>> media.say("Hello, world!")
    Hello, world!
    >>> 

Perfect!

.. This is probably a little advanced for the target audience...
    A bit more about AMP
    ====================

    As mentioned before, AMP stands for the Asynchronous Messaging Protocol. It
    was developed by programmers at `Twisted Matrix Labs 
    <http://twistedmatrix.com/>`_ , who wanted a simple and useful implementation
    of a completely asynchronous, bidirectional, remote procedure call system.

    Asynchronous
    ------------

    .. warning:: This is complicated.

        You aren't really expected to understand deferred/asynchronous computation
        after this, but it'd be nice if you had an idea about it. If you want to
        learn more, Dave Peticolas has an 
        `excellent series of articles <http://krondo.com/blog/?page_id=1327>`_
        that can teach you the Twisted way.

    When introduced to networking, most people are taught **synchronous**
    communication. Synchronous communication is where you send a networked message,
    and you don't continue on in your program until the message is fully sent and
    has been received by the other side.

    For example, the python `urllib <http://docs.python.org/library/urllib>`_
    module is synchronous. If someone wanted to write a webpage
    to a file, they might do it something like this::

        def download_webpage(url, f):
            response = urllib.urlopen(url)
            f.write(response.read())
            f.close()

    This reads the entire webpage into memory. As soon as the webpage is fully in
    memory, it is written to a file, and the file is then closed.

    The operating system will manage the connection and download
    the file until the connection is terminated by the HTTP server. During that
    time, Python sits waiting and can't do anything
    sle -- response.read is a **blocking call**.

    On the other hand, an asynchronous solution using Twisted could look something
    like this::

        def download_webpage(url, f):
            twisted.web.client.getPage(url).addCallback(f.write).addCallback(lambda _: f.close)

    This tells Twisted to start downloading the webpage, and when it has the whole
    thing in memory, call f.write with the page contents as the only argument 
    (i.e. write the page to the file), and then call f.close

    Twisted will manage the connection and download the file in pieces. Whenever
    the operating system says that the server has sent more data, Twisted grabs that
    data from the connection and stores it, until the connection is closed. During
    that time, the application can continue to make more web requests or do more
    calculations, as long as it gives the Twisted event loop time to check the
    connection status and so on every once in a while.

    :py:func:`getPage` returns a `deferred <http://twistedmatrix.com/documents/current/core/howto/defer.html>`_
    value, which doesn't immediately have something to show. As soon as it does,
    though, the callbacks are told that the deferred has "fired" and a real value
    is ready.

    Right, but what about AMP?
    ..........................

    In AMP, every RPC call is asynchronous. You can send multiple RPC calls off,
    and their results may arrive in any order. This is AMP's purpose, this is all
    it does: provide a way to pass dicts (values) and exceptions (errors)
    in an independent order, whenever they are ready, without ever stopping
    work just to wait for a response.

    Well, actually...
    .................

    As you may have noticed, :py:mod:`media` is *not* asynchronous, it is 
    synchronous. You call :py:func:`media.show` and a picture is shown, and only
    *then* does it return -- there is no callback to get notified when the picture
    shows up. Not even behind the scenes.

    While AMP may be an asynchronous protocol on paper, *Ampy* includes a partial
    implementation of AMP that is synchronous. This greatly simplifies the
    client side of the equation. However, the server side (running the GUI etc.)
    is still asynchronous and nonblocking.

    As a consequence of this, it's required that GUI servers only serve one client
    at a time. That way they can act just as blockingly as the client, without
    locking out other clients that are waiting for a chance. For example, we can
    put everything on hold while waiting for a dialog box to close.

    Bidirectional
    =============

    .. todo:: Write me! WRIIIIITE MEEEEE!

Tkinterizing
============

.. todo:: Write this