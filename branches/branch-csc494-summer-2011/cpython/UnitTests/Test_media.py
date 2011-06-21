"""Unit tests for media.py

Most of anything media.py does is hide the existence of other modules,
and forward calls to them. A proper unit test, then, only tests that the
forwarding is done correctly. That's what is done here.

"""
import nose
import media
import mediawindows as mw

def t_tuple(t):
    if len(t) == 2:
        func, replmod = t
        replfname = func.__name__
    elif len(t) == 3:
        func, replmod, replfname = t

    original_func = getattr(replmod, replfname)
    calls = []
    def new_func(*args, **kwargs):
        calls.append((tuple(args), kwargs))

    setattr(replmod, replfname, new_func)

    try:
        func()
    finally:
        setattr(replmod, replfname, original_func)

    assert len(calls) == 1
    assert calls[0] == ((), {})

def generate_simple_forwarding_tests(tests):
    """Given a list of tests, return a test generator usable by nose

    `tests` is an iterable of tuples, where each tuple is of the form:

        (function, module, forwarded_function_name)

    e.g. if media.py contains the following code::

        def poop(*args, **kwargs):
            mediawindows.poop(*args, **kwargs)

    then you want the following test tuple::

        (media.poop, mediawindows, 'poop')

    the resulting test will check whether media.poop calls mediawindows.poop
    with the same arguments it received (none!)

    For convenience, if the forwarded function is named the same as the
    media.py function, you can provide a 2-tuple instead.
    The following two test tuples are equivalent:

        - (media.poop, mediawindows, media.poop.__name__)
        - (media.poop, mediawindows)

    """

    def test_generator():
        for t in tests:
            yield t_tuple, t

    return test_generator

test_chooses = generate_simple_forwarding_tests([
    (media.choose_save_filename, mw),
    (media.choose_file, mw),
    (media.choose_folder, mw),
    (media.choose_color, mw)])


# dunno how else to get nose to not run it...
generate_simple_forwarding_tests.__test__ = False
