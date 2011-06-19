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

`arguments` is a list of :samp:`{key}, {AmpType}` pairs. :mod:`ampy` has a lot
of types for representing Python values, including:

 - :py:class:`ampy.amp.Integer`
 - :py:class:`ampy.amp.Float`
 - :py:class:`ampy.amp.Boolean`
 - :py:class:`ampy.amp.String`
 - :py:class:`ampy.amp.Unicode`

In addition, :py:mod:`mediawindows.amp` offers the following extra AMP types:

 - :py:class:`mediawindows.amp.BigString`
 - :py:class:`mediawindows.amp.BigUnicode`
 - :py:class:`mediawindows.amp.PILImage`

Each of these let you pass in Python values of that type and get the same
value back on the other side of the AMP connection.

.. _AMP: http://amp-protocol.net/
.. _show: http://www.pythonware.com/library/pil/handbook/image.htm#Image.show
.. _pygame: http://www.pygame.org/
.. _here: http://code.google.com/p/pygraphics/wiki/MacInstall
.. _known: http://docs.python.org/library/threading.html#importing-in-threaded-code
.. _ampy: https://launchpad.net/ampy