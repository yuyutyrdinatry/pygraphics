from __future__ import absolute_import

from . import amp
from .client import init_mediawindows, callRemote
from .proxy import choose_save_filename, choose_file, choose_folder, choose_color

_MEDIAWINDOWS_INITIALIZED = False # this will get changed later
