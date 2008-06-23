import tkSnack
from sample import *
import os
import math

class Sound(object):
    '''A Sound class as a wrapper for the tkSnack object.'''
    
    # This is the default frequency of samples per second played
    default_samp_rate = 22050
    
    # This is the default encoding of 16 bits per sample 
    # allowing a maximum of 32767 and a minimum of -32768 as pressure values
    default_encoding = "Lin16"
    default_channels = 1

    def __init__(self, seconds=None, samples=None, filename=None, channels=None):
        '''Create a Sound.
        
        Requires one of:
        - int seconds, e.g. Sound(10) 
        - named in argument samples, e.g. Sound(samples=2000)
        - named str argument filename, e.g. Sound(filename='sound.wav').'''
        
        self.set_filename(filename)
        self.channels = channels or self.default_channels
        
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
        self.set_tk_sound(snd)
            
            
    def __str__(self):
        '''Return a str for this Sound with its length.'''
        
        return "Sound of length " + str(len(self))


    def __iter__(self):
        '''Return this Sound's Samples from start to finish.'''
        
        if self.channels == 1:
            for i in range(0, len(self)):
                yield MonoSample(self.tk_sound, i)
        elif self.channels == 2:
            for i in range(0, len(self)):
                yield StereoSample(self.tk_sound, i)
        else:
            raise ValueError('Number of channels invalid')


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
        '''Append s seconds of silence in all channels to the end 
        of this Sound.'''
        
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

        if 0 <= i <= len(self) - 1:
            if self.channels == 1:
                return MonoSample(self.tk_sound, i)
            elif self.channels == 2:
                return StereoSample(self.tk_sound, i)
            else:
                raise ValueError('Number of channels invalid')
        else:
            raise IndexError

    
    def get_max(self):
        '''Return this Sound's largest sample value.'''
        
        largest = 0
        for sample in self:
            if self.channels == 1:
                if largest < sample.get_value():
                    largest = sample.get_value()
            if self.channels == 2:
                if largest < sample.get_left() + sample.get_right():
                    largest = sample.get_left() + sample.get_right()
        return largest
       
        
    def get_min(self):
        '''Return this Sound's largest sample value.'''
        
        smallest = 0
        for sample in self:
            if self.channels == 1:
                if smallest > sample.get_value():
                    smallest = sample.get_value()
            if self.channels == 2:
                if smallest > sample.get_left() + sample.get_right():
                    smallest = sample.get_left() + sample.get_right()
        return smallest


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


def sine_wave(freq, amp, sec):
    '''Return a synthesized sound of sec seconds in the form of a sine wave 
    with frequency freq in Hz and amplitude amp in the range [0, 32767].'''
    
    new_snd = Sound(seconds=sec)
    rate = new_snd.get_sampling_rate()
    interval = 1.0 / freq
    samples_per_cycle = rate * interval
    max_cycle = 2 * math.pi
    
    for i in range(len(new_snd)):
        curr = new_snd.get_sample(i)
        raw_val = math.sin((i / samples_per_cycle) * max_cycle)
        curr.set_value(int(raw_val * amp))
    
    return new_snd


def square_wave(freq, amp, sec):
    '''Return a synthesized sound of sec seconds in the form of a square wave 
    with frequency freq in Hz and amplitude amp in the range [0, 32767].'''

    new_snd = Sound(seconds=sec)
    rate = new_snd.get_sampling_rate()
    interval = 1.0 / freq
    samples_per_cycle = rate * interval
    samples_per_halfcycle = int(samples_per_cycle / 2)
    sample_val = amp
    
    s = 0
    for i in range(len(new_snd)):
        if s > samples_per_halfcycle:
            sample_val = sample_val * -1
            s = 0
        
        curr = new_snd.get_sample(i)
        curr.set_value(int(sample_val))
        s += 1

    return new_snd


def add_sounds(snd1, snd2):
    smaller = min(len(snd1), len(snd2))
    new_sound = Sound(samples=smaller)
    
    for i in range(len(new_sound)):
        source1 = snd1.get_sample(i)
        source2 = snd1.get_sample(i)
        new_samp = new_sound.get_sample(i)
        new_samp.set_value(source1.get_value() + source2.get_value())
        
    return new_sound
        
        
if __name__ == '__main__':
    import Tkinter as tk

    root = tk.Tk()
    root.withdraw()
    tkSnack.initializeSnack(root)
    
    s1 = Sound(filename='/work/01 Smack That [feat. Eminem].mp3', channels=2)
    
    def normalize(snd):
        max_samp = snd.get_max()
        min_samp = snd.get_min()
        
        divider = max(abs(max_samp), abs(min_samp))

        multiplier = 32767.0 / divider
        for sample in snd:
            new_val = sample.get_value() * multiplier
            sample.set_value(int(new_val))
    
    def decrease_vol(snd, factor):
        
        for sample in snd:
            new_val = sample.get_value() * factor
            sample.set_value(int(new_val))
            
            
    def echo(snd, delay):
        
        source = snd.copy()
        
        for i in range(delay, len(snd)):
            source_samp = source.get_sample(i - delay)
            target_samp = snd.get_sample(i)

            echo_val = 0.3 * source_samp.get_value()
            target_samp.set_value(echo_val + target_samp.get_value())
        
        return snd
    
    
    def plot_waveform(snd, width=1024, height=300):
   
        win = tk.Toplevel()
    
        c = tkSnack.SnackCanvas(win, background="#060", width=width, height=height)
        c.pack()
        c.create_waveform(0, 0, fill="#0f0" , sound=snd.tk_sound, width=width, height=height, zerolevel=1)

    def plot_spectrogram(snd, width=1024, height=300):
    
        win = tk.Toplevel()
    
        c = tkSnack.SnackCanvas(win, background="#060", width=width, height=height)
        c.pack()
        c.create_spectrogram(0, 0, sound=snd.tk_sound, width=width, height=height)
    
    
    def plot_spectrum(snd, width=1024, height=300):
        
        win = tk.Toplevel()
    
        c = tkSnack.SnackCanvas(win, background="#060",width=width, height=height)
        c.pack()
        c.create_section(0, 0, fill="#0f0", sound=snd.tk_sound, width=width, height=height)
