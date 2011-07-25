import os
from functools import partial

import mediawindows as mw

LAST_OPENED_DIRECTORY = os.getcwd()

def _choose_with_remote(command):
    global LAST_OPENED_DIRECTORY

    try:
        path = mw.callRemote(command, initialdir=LAST_OPENED_DIRECTORY)['path']
    except:
        return None
    else:
        LAST_OPENED_DIRECTORY = os.path.dirname(path)
        return path

choose_save_filename = partial(
    _choose_with_remote, 
    mw.amp.AskSaveasFilename)

choose_file = partial(
    _choose_with_remote, 
    mw.amp.AskOpenFilename)

choose_folder = partial(
    _choose_with_remote, 
    mw.amp.AskDirectory)

def choose_color():
    '''Prompt user to pick a color. Return a RGB Color object.'''

    colors = mw.callRemote(mw.amp.AskColor, r=255, g=255, b=255)
    return (colors['r'], colors['g'], colors['b'])

def say(text):
    mw.callRemote(mw.amp.Say, text=text)
