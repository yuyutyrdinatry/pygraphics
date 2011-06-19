from __future__ import absolute_import

from . import amp
from .client import init_mediawindows, callRemote

_MEDIAWINDOWS_INITIALIZED = False # this will get changed later

__all__ = [
    'amp',
    'init_mediawindows',
    'callRemote']
