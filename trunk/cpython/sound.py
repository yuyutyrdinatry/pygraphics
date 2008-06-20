import tkSnack
from sample import *
import os

class Sound(object):
    '''A Sound class as a wrapper for the tkSnack object.'''
    
    default_frequency = 22050

    def __init__(self, seconds=None, samples=None, filename=None):
        '''Create a Sound.
        
        Requires one of:
        - int seconds, e.g. Sound(10) 
        - named in argument samples, e.g. Sound(samples=2000)
        - named str argument filename, e.g. Sound(filename='sound.wav').'''
        
        self.set_filename(filename)
        
        if filename != None:
            snd = tkSnack.Sound(load=filename)
        elif samples != None:
            snd = tkSnack.Sound()
            snd.configure(frequency=self.default_frequency)
            snd.length(samples)
        elif seconds != None:
            snd = tkSnack.Sound()
            snd.configure(frequency=self.default_frequency)
            samples = int(seconds * self.default_frequency)
            snd.length(samples)
        else:
            raise TypeError("No arguments were given to the Sound constructor.")
        
        self.set_tk_sound(snd)
            
            
    def __str__(self):
        '''Return a str for this Sound with its length.'''
        
        return "Sound of length " + str(len(self))


    def __iter__(self):
        '''Return this Sound's Samples from start to finish.'''
        
        for i in range(0, len(self)):
            yield Sample(self, i)


    def __len__(self):
        '''Return the number of Samples in this Sound.'''
        
        return self.tk_sound.length()


    def set_tk_sound(self, tk_snd):
        '''Set this Sound's tkSnack Sound object.'''
        
        self.tk_sound = tk_snd
        
        
    def get_tk_sound(self):
        '''Return this Sound's tkSnack Sound object.'''
        
        return self.tk_sound


    def copy(self):
        '''Return a deep copy of this Sound.'''
        
        samples = len(self)
        new_snd = Sound(samples=samples)
        new_snd.tk_sound.copy(self.tk_sound)
        return new_snd


    def append_silence(self, s):
        '''Append s seconds of silence to the end of this Sound.'''
        
        new_samples = len(self) + (s * self.get_sampling_rate())
        self.tk_sound.length(new_samples)


    def insert(self, snd, i):
        '''Insert Sound snd at index i.'''
        
        self.tk_sound.insert(snd.get_tk_sound(), i)


    def crop(self, first, last):
        '''Crop this Sound so that all Samples before int first and 
        after int last are removed.'''
        
        self.tk_sound.crop(start=first, end=last)


    def play(self, first=0, last=-1, blocking=0):
        '''Play this sound from sample at first to sample at last. Play entire
        Sound as default. If blocking is a non-zero number do not return until
        Sound has finished playing.'''

        self.tk_sound.play(blocking=blocking, start=first, end=last)


    def stop(self):
        '''Stop playing this Sound.'''
        
        self.tk_sound.stop()
        

    def get_sampling_rate(self):
        '''Return the number of Samples this Sound plays per second.'''

        return self.tk_sound["frequency"]


    def set_sampling_rate(self, freq):
        '''Set the number of Samples this Sound plays per second to
        the int freq.'''
        
        self.tk_sound.configure(frequency=freq)


    def get_sample(self, i):
        '''Return the Sample object at index i.'''

        if i < len(self) - 1:
            return Sample(self.tk_sound, i)
        else:
            raise IndexError

        
    def set_filename(self, filename):
        '''Set this Sound's filename to filename. If filename is None 
        set this Sound's filename to the empty string.'''
        
        if filename:
            self.filename = filename
        else:
            self.filename = ''
    
    
    def get_filename(self):
        '''Return this Sound's filename.'''

        return self.filename
        
        
    def save_as(self, filename):
        '''Save this Sound to filename filename and set its filename.'''
        
        self.set_filename(filename)
        self.tk_sound.write(filename)

    
    def save(self):
        '''Save this Sound to its filename.'''
        
        self.tk_sound.write(self.filename)
        
        
if __name__ == '__main__':
    
    s1 = Sound(filename='/Users/chris/Documents/PyGraphics/Workspace/raven.wav')
    s2 = Sound(10)