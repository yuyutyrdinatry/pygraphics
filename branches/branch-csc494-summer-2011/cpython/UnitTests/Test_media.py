"""Unit tests for media.py

Most of anything media.py does is hide the existence of other modules,
and forward calls to them. A proper unit test, then, only tests that the
forwarding is done correctly. That's what is done here. Of course, that's crazy.

"""
# <_ssbr> bob2: it tests whether the "show" method is called, with no parameters
#         on the argument passed to the show function.
# <bob2>  _ssbr: ok, mocks have definitely gone to your brain

# (omitted: "<_ssbr> these functions need integration tests, not unit tests :(")

import nose
import media
import mediawindows as mw

def t_tuple(t):
    if len(t) == 2:
        func, replmod = t
        replfname = func.__name__
    else:
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

    assert calls == [((), {})]

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

def t_genericfunc(t):
    args = ((), {})
    if len(t) == 1:
        func, = t
        attr = None
    elif len(t) == 2:
        func, attr = t
    else:
        func, attr, args = t

    if attr is None:
        attr = func.__name__

    calls = []
    class Proxy(object):
        pass

    setattr(Proxy, attr, staticmethod(
        lambda *args, **kwargs: 
            calls.append((args, kwargs))))

    func(Proxy, *args[0], **args[1])
    assert calls == [args]

def generate_genericfunction_tests(tests):
    """Given a list of tests, return a test generator usable by nose.

    genericfunction-tests are those that test whether foo(obj)<->obj.foo()

    `tests` is an iterable of tuples, where each tuple is of the form:

        (function, attribute)

    e.g. if media.py contains the following code::

        def poop(obj):
            obj.poop()

    then you want the following test tuple::

        (media.poop, 'poop')

    or, better, ``(media.poop,)``, by the same idiom as 
    generate_simple_forwarding_tests.

    Because it's actually needed, a third parameter is also available.
    The arguments passed to obj.method can be determined as a third element,
    a pair (args, kwargs), where function(*args, **kwargs) will be called.

    """
    def test_generator():
        for t in tests:
            yield t_genericfunc, t

    return test_generator

test_chooses = generate_simple_forwarding_tests([
    (media.choose_save_filename, mw),
    (media.choose_file, mw),
    (media.choose_folder, mw),
    (media.choose_color, mw)])

test_picture = generate_genericfunction_tests([
    (media.crop_picture, 'crop', ((1, 2, 3, 4), {})),
    (media.get_pixel, None, ((1, 2), {})),
    (media.get_width,),
    (media.get_height,),
    (media.show,),
    (media.show_external,),
    (media.update,),
    (media.close,),
    ##(media.add_line, 'add_line', ((1, 2, 3, 4, 5), {})), these get reordered
    ##(media.add_line, 'add_line', ((1, 2, 3, 4, 5), {})),
    ])

test_pixels = generate_genericfunction_tests([
    (media.set_red, None, ((1,), {})),
    (media.get_red,),
    (media.set_green, None, ((1,), {})),
    (media.get_green,),
    (media.set_blue, None, ((1,), {})),
    (media.get_blue,),
    (media.get_color,),
    (media.set_color, None, ((1,), {})),
    (media.get_x,),
    (media.get_y,),
    ])

test_color = generate_genericfunction_tests([
    (media.distance, None, ((1,), {})),
    (media.darken, 'make_darker'),
    (media.lighten, 'make_lighter'),
    ])

# dunno how else to get nose to not run it...
generate_simple_forwarding_tests.__test__ = False
generate_genericfunction_tests.__test__ = False
