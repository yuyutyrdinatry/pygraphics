from __future__ import absolute_import

from . import amp
from .threads import init_mediawindows, threaded_callRemote

_THREAD_RUNNING = False # this will get changed by threads

__all__ = [
    'amp',
    'init_mediawindows',
    'threaded_callRemote',
    '_THREAD_RUNNING']
