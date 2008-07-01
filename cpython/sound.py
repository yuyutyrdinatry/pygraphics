import tkSnack
from sample import *
import os
import math
try:
    tester = tkSnack.Sound()
    del tester
except RuntimeError:
    import Tkinter as tk
    root = tk.Tk()
    root.withdraw()
    tkSnack.initializeSnack(root)


class Sound(object):
    '''A Sound class as a wrapper for the tkSnack object.'''
    
    # This is the default frequency of samples per second played
    default_samp_rate = 22050
    
    # This is the default encoding of 16 bits per sample 
    # allowing a maximum of 32767 and a minimum of -32768 as pressure values
    default_encoding = "Lin16"
    channels = 1
    
    def __init__(self, stereo=False, filename=None, samples=None, seconds=None):
        '''Create a Sound. Specify stereo as a boolean value, 
        otherwise mono as default.
        
        Requires one of:
        - int seconds, e.g. Sound(seconds=10) 
        - named in argument samples, e.g. Sound(samples=2000)
        - named str argument filename, e.g. Sound(filename='sound.wav').
        
        Filename takes precedence over samples, which take precedence 
        over seconds.'''
        
        self.set_filename(filename)
        if stereo:
            self.channels = 2
        
        if filename != None:
            snd = tkSnack.Sound(load=filename)
        elif samples != None:
            snd = tkSnack.Sound()
            snd.length(samples)
        elif seconds != None:
            snd = tkSnack.Sound()
            samples = int(seconds * self.default_samp_rate)
            snd.length(samples)
        else:
            raise TypeError("No arguments were given to the Sound constructor.")
        
        snd.convert(format=self.default_encoding, 
                    frequency=self.default_samp_rate,
                    channels=self.channels)
        
        # convert method appends a few 0 value samples
        if samples or seconds:
            snd.crop(0, samples -1)
            
        self.set_tk_sound(snd)
            
            
    def __str__(self):
        '''Return the number of Samples in this Sound as a str.'''
        
        return "Sound of length " + str(len(self))


    def __iter__(self):
        '''Return this Sound's Samples from start to finish.'''
        
        if self.channels == 1:
            for i in range(0, len(self)):
                yield MonoSample(self.tk_sound, i)
        elif self.channels == 2:
            for i in range(0, len(self)):
                yield StereoSample(self.tk_sound, i)
                

    def __len__(self):
        '''Return the number of Samples in this Sound.'''
        
        return self.tk_sound.length()

    def __add__(self, snd):
        '''Return a Sound object with this Sound followed by Sound snd.'''
        
        new = self.copy()
        new.append(snd)
        return new


    def __mul__(self, num):
        '''Return a Sound object with this Sound repeated num times.'''
        
        new = self.copy()
        for time in range(int(num) - 1):
            new.append(self)
        return new


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
        '''Append s samples of silence to each of this Sound's channels.
        If s is negative remove s samples from the end of this Sound.'''
        
        total_samples = len(self) + s
        self.tk_sound.length(total_samples)
        #check if s is negative


    def append(self, snd):
        '''Append Sound snd to this Sound. Requires that snd has same number of
        channels as this Sound.'''
        
        self.tk_sound.concatenate(snd.get_tk_sound())


    def insert(self, snd, i):
        '''Insert Sound snd at index i. Requires that snd has same number of
        channels as this Sound.'''

        # Negative indices are supported
        if -len(self) <= i <= len(self) - 1:            
            i = i % len(self)
            self.tk_sound.insert(snd.get_tk_sound(), i)
        else:
            raise IndexError('Sample value out of bounds.')


    def crop(self, first, last):
        '''Crop this Sound so that all Samples before int first and 
        after int last are removed. Cannot crop to a single sample.'''

        # Negative indices are supported
        if -len(self) <= first <= len(self) - 1 and \
            -len(self) <= last <= len(self) - 1: 
            
            first = first % len(self)
            last = last % len(self)
            self.tk_sound.crop(start=first, end=last)
        else:
            raise IndexError('Sample value out of bounds.')


    def play(self, first=0, last=-1):
        '''Play this sound from index first to index last. Play entire
        Sound as default. If blocking is True do not return until Sound 
        has finished playing.'''
        
        # Negative indices are supported
        if -len(self) <= first <= len(self) - 1 and \
            -len(self) <= last <= len(self) - 1: 
            
            first = first % len(self)
            last = last % len(self)
            self.tk_sound.play(blocking=False, start=first, end=last)
        elif len(self) == 0:
            pass
        else:
            raise IndexError('Sample value out of bounds.')


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
        '''Return this Sound's Sample object at index i.'''

        if self.channels == 1:
            return MonoSample(self.tk_sound, i)
        elif self.channels == 2:
            return StereoSample(self.tk_sound, i)

    
    def get_max(self):
        '''Return this Sound's highest sample value. If this Sound is stereo
        return the absolute highest for both channels.'''
        
        largest = 0
        if self.channels == 1:
            for sample in self:
                if largest < sample.get_value():
                        largest = sample.get_value()
        if self.channels == 2:
            for sample in self:
                if largest < max(sample.get_left(), sample.get_right()):
                    largest = max(sample.get_left(), sample.get_right())
        return largest
       
        
    def get_min(self):
        '''Return this Sound's lowest sample value. If this Sound is stereo
        return the absolute lowest for both channels.'''
        
        smallest = 0
        if self.channels == 1:
            for sample in self:
                if smallest > sample.get_value():
                    smallest = sample.get_value()
        if self.channels == 2:
            for sample in self:
                if smallest > min(sample.get_left(), sample.get_right()):
                    smallest = min(sample.get_left(), sample.get_right())
        return smallest


    def get_channels(self):
        '''Return the number of channels in this Sound.'''
        
        return self.tk_sound['channels']
    

    def set_filename(self, filename=None):
        '''Set this Sound's filename to filename. If filename is None 
        set this Sound's filename to the empty string.'''
        
        if filename != None:
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


def make_sine_wave(freq, amp, samp):
    '''Return a synthesized sound samp samples long in the form of a sine wave 
    with frequency freq in Hz and amplitude amp in the range [0, 32767].'''
    
    new_snd = Sound(samples=samp)
    rate = new_snd.get_sampling_rate()
    period = 1.0 / freq
    samples_per_period = rate * period
    max_cycle = 2 * math.pi
    
    for i in range(samp):
        curr = new_snd.get_sample(i)
        raw_val = math.sin((i / samples_per_period) * max_cycle)
        curr.set_value(int(raw_val * amp))
    
    return new_snd


def make_square_wave(freq, amp, samp):
    '''Return a synthesized sound samp samples long in the form of a square wave 
    with frequency freq in Hz and amplitude amp in the range [0, 32767].'''

    new_snd = Sound(samples=samp)
    rate = new_snd.get_sampling_rate()
    period = 1.0 / freq
    samples_per_period = rate * period
    samples_per_halfperiod = int(samples_per_period / 2)
    sample_val = amp
    
    s = 0
    for i in range(samp):
        if s > samples_per_halfperiod:
            sample_val = sample_val * -1
            s = 0
        
        curr = new_snd.get_sample(i)
        curr.set_value(int(sample_val))
        s += 1

    return new_snd


def make_triangle_wave(freq, amp, samp):
    '''Return a synthesized sound samp samples long in the form of a square wave 
    with frequency freq in Hz and amplitude amp in the range [0, 32767].'''

    new_snd = Sound(samples=samp)
    rate = new_snd.get_sampling_rate()
    period = 1.0 / freq
    samples_per_period = rate * period
    samples_per_halfperiod = int(samples_per_period / 2)
    samples_per_quarterperiod = int(samples_per_period / 4)
    increment = int(amp / samples_per_quarterperiod)
    sample_val = 0
    
    quarter_period = 0
    half_period = 0

    for i in range(samp):
        
        if quarter_period > samples_per_quarterperiod:
            increment = increment * -1
            quarter_period = 0
        if half_period > samples_per_halfperiod:
            increment = increment * -1
            half_period = 0
        
        curr = new_snd.get_sample(i)
        sample_val = sample_val + increment
        curr.set_value(int(sample_val))
        
        quarter_period += 1
        half_period += 1

    return new_snd

C = make_sine_wave(264, 6000, 11025)
D = make_sine_wave(297, 6000, 11025)
E = make_sine_wave(330, 6000, 11025)
F = make_sine_wave(352, 6000, 11025)
G = make_sine_wave(396, 6000, 11025)
A = make_sine_wave(440, 6000, 11025)
B = make_sine_wave(494, 6000, 11025)