from __future__ import absolute_import

from . import amp
from .amp import init_mediawindows, threaded_callRemote

_THREAD_RUNNING = False # this will get changed by amp

__all__ = [
    'amp',
    'init_mediawindows',
    'threaded_callRemote',
    '_THREAD_RUNNING']
