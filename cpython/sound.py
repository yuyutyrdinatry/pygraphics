'''The Sound class and helper functions. This currently supports only 
uncompressed .wav files. For best quality use .wav files with sampling
rates of either 22050 or 44100. The default number of channels,
sampling rate, encoding, and buffering can be changed in the sound.py
file.'''

from pygraphics.sample import *
import math
import numpy
import pygame
import wave
import sndhdr
import os

####################------------------------------------------------------------
## Defaults
####################------------------------------------------------------------

SOUND_FORMATS = ['.wav']
DEFAULT_SAMP_RATE = 44100
DEFAULT_ENCODING = -16
DEFAULT_CHANNELS = 2
DEFAULT_BUFFERING = 3072
pygame.mixer.pre_init(DEFAULT_SAMP_RATE, 
                      DEFAULT_ENCODING, 
                      DEFAULT_CHANNELS, 
                      DEFAULT_BUFFERING)
pygame.mixer.init()
#else:
#    DEFAULT_SAMP_RATE = DEFAULTS[0]
#    DEFAULT_ENCODING = DEFAULTS[1]
#    
#    # pygame.mixer.get_init() returns channels 0-based, 1 channel is 0, 2 is 1
#    DEFAULT_CHANNELS = DEFAULTS[2] + 1

AUDIO_ENCODINGS = { 8 : numpy.uint8,   # unsigned 8-bit
     16 : numpy.uint16, # unsigned 16-bit
     -8 : numpy.int8,   # signed 8-bit
     -16 : numpy.int16  # signed 16-bit
     }

####################------------------------------------------------------------
## Sound object
####################------------------------------------------------------------


class Sound(object):
    '''A Sound class as a wrapper for the pygame.mixer.Sound object.'''
        
    def __init__(self, filename=None, samples=None, seconds=None, sound=None):
        '''Create a Sound.
                
        Requires one of:
        - named str argument filename (with .wav extension), 
                e.g. Sound(filename='sound.wav')
        - named int argument samples, e.g. Sound(samples=2000)
        - named int argument seconds, e.g. Sound(seconds=10) 
        - named pygame.mixer.Sound argument sound, 
                e.g. Sound(sound=pygame.mixer.Sound)
        
        Filename takes precedence over samples, which take precedence 
        over seconds, which in turn takes precedence over sound.'''
        
        self.channels = DEFAULT_CHANNELS
        self.samp_rate = DEFAULT_SAMP_RATE
        self.numpy_encoding = AUDIO_ENCODINGS[DEFAULT_ENCODING]
        self.encoding = DEFAULT_ENCODING
        self.set_filename(filename)
        
        if filename != None:
            snd = load_pygame_sound(filename)
            
        elif samples != None:
            snd = create_pygame_sound(samples)
            
        elif seconds != None:
            samples = int(seconds * self.samp_rate)
            snd = create_pygame_sound(samples)
            
        elif sound != None:
            snd = sound
            
        else:
            raise TypeError("No arguments were given to the Sound constructor.")
                    
        self.set_pygame_sound(snd)
            
            
    def __str__(self):
        '''Return the number of Samples in this Sound as a str.'''
        
        return "Sound of length " + str(len(self))


    def __iter__(self):
        '''Return this Sound's Samples from start to finish.'''
        
        if self.channels == 1:
            for i in range(len(self)):
                yield MonoSample(self.samples, i)
        elif self.channels == 2:
            for i in range(len(self)):
                yield StereoSample(self.samples, i)
                

    def __len__(self):
        '''Return the number of Samples in this Sound.'''
        
        return len(self.samples)


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


    def set_pygame_sound(self, pygame_snd):
        '''Set this Sound's pygame Sound object.'''
        
        self.pygame_sound = pygame_snd
        
        # self.samples is a numpy array object (either 1D or 2D depending on the
        # number of channels). This object allows access to specific samples
        # in the buffer.
        self.samples = pygame_to_sample_array(pygame_snd)
        self.player = None
        
        
    def get_pygame_sound(self):
        '''Return this Sound's pygame Sound object.'''
        
        return self.pygame_sound


    def copy(self):
        '''Return a deep copy of this Sound.'''
        
        samples = self.samples.copy()
        new_pygame_snd =  sample_array_to_pygame(samples)
        return Sound(sound=new_pygame_snd)


    def append_silence(self, s):
        '''Append s samples of silence to each of this Sound's channels.'''
        
        if self.channels == 1:
            silence_array = numpy.zeros(s, self.numpy_encoding)
        else:
            silence_array = numpy.zeros((s, 2), self.numpy_encoding)
        pygame_silence =  sample_array_to_pygame(silence_array)
        self.append(Sound(sound=pygame_silence))


    def append(self, snd):
        '''Append Sound snd to this Sound. Requires that snd has same number of
        channels as this Sound.'''
        
        if self.get_channels() == snd.get_channels():
            snd_samples = pygame_to_sample_array(snd.get_pygame_sound())
            my_samples = self.samples
            new_samples = numpy.concatenate((my_samples, snd_samples))
            self.set_pygame_sound(sample_array_to_pygame(new_samples))
        else:
            raise ValueError('Sound snd must have same number of channels.')
    
    
    def insert(self, snd, i):
        '''Insert Sound snd at index i. Requires that snd has same number of
        channels as this Sound. Negative indices are supported.'''

        if self.get_channels() == snd.get_channels() == 1:
            first_chunk = self.samples[:i]
            second_chunk = self.samples[i:]
            new_samples = numpy.concatenate((first_chunk, 
                                             snd.sound_array, 
                                             second_chunk))
            self.set_pygame_sound(sample_array_to_pygame(new_samples))
        elif self.get_channels() == snd.get_channels() == 2:
            first_chunk = self.samples[:i, :]
            second_chunk = self.samples[i:, :]
            new_samples = numpy.vstack((first_chunk, 
                                        snd.sound_array, 
                                        second_chunk))
            
            self.set_pygame_sound(sample_array_to_pygame(new_samples))
        else:
            raise ValueError("Sound snd must have same number of channels.")


    def crop(self, first, last):
        '''Crop this Sound so that all Samples before int first and 
        after int last are removed. Cannot crop to a single sample. 
        Negative indices are supported'''

        # Negative indices are supported
        first = first % len(self)
        last = last % len(self)
        
        new_samples = self.samples[first:last + 1]
        self.set_pygame_sound(sample_array_to_pygame(new_samples))


    def play(self, first=0, last=-1):
        '''Play this Sound from sample index first to last. As default play
        the entire Sound.'''
        
        self.player = self.copy()
        self.player.crop(first, last)
        self.player.get_pygame_sound().play()


    def stop(self):
        '''Stop playing this Sound.'''
        
        if self.player:
            self.player.get_pygame_sound().stop()
        

    def get_sampling_rate(self):
        '''Return the number of Samples this Sound plays per second.'''

        return self.samp_rate


    def get_sample(self, i):
        '''Return this Sound's Sample object at index i. Negative indices are
        supported. Negative indices are supported.'''

        if self.channels == 1:
            return MonoSample(self.samples, i)
        elif self.channels == 2:
            return StereoSample(self.samples, i)

    
    def get_max(self):
        '''Return this Sound's highest sample value. If this Sound is stereo
        return the absolute highest for both channels.'''
        
        return self.samples.max()
        
        
    def get_min(self):
        '''Return this Sound's lowest sample value. If this Sound is stereo
        return the absolute lowest for both channels.'''
        
        return self.samples.min()


    def get_channels(self):
        '''Return the number of channels in this Sound.'''
        
        return self.channels
    

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
        
        ext = os.path.splitext(filename)[-1]
        if ext in SOUND_FORMATS or ext in [e.upper() for e in SOUND_FORMATS]:
            self.set_filename(filename=filename)
            wav = wave.open(filename, 'w')
            wav.setnchannels(self.get_channels())
            
            # calculate the number of bytes for this sound
            fmtbytes = (abs(self.encoding) & 0xff) >> 3
            wav.setsampwidth(fmtbytes)
            
            wav.setframerate(self.get_sampling_rate())
            wav.setnframes(len(self))
            wav.writeframes(self.pygame_sound.get_buffer().raw)
            wav.close()
        else:
            raise ValueError("%s is not one of the supported file formats." \
                             % ext)        
        
        
    def save(self):
        '''Save this Sound to its filename. If an extension is not specified
        the default is .wav.'''
 
        filename = os.path.splitext(self.get_filename())[0]
        ext = os.path.splitext(self.get_filename())[-1]
        if ext == '':
            self.save_as(filename + '.wav')
        else:
            self.save_as(self.get_filename())
        
        
####################------------------------------------------------------------
## Note class
####################------------------------------------------------------------


class Note(Sound):
    '''A Note class to create different notes of the C scale. Inherits from Sound,
    does everything Sounds do, and can be combined with Sounds.'''
    
    frequencies = {'C' : 264,
                   'D' : 297,
                   'E' : 330,
                   'F' : 352,
                   'G' : 396,
                   'A' : 440,
                   'B' : 494}
    
    default_amp = 6000
    
    def __init__(self, note, s, octave=0):
        '''Create a Note s samples long with the frequency according to 
        str note. The following notes are available, starting at middle C:
        
        'C', 'D', 'E', 'F', 'G', 'A', and 'B'
        
        To raise or lower an octave specify the argument octave as a
        positive or negative int. Positive to raise by that many octaves
        and negative to lower by that many.'''
        
        self.channels = DEFAULT_CHANNELS
        self.samp_rate = DEFAULT_SAMP_RATE
        self.numpy_encoding = AUDIO_ENCODINGS[DEFAULT_ENCODING]
        self.encoding = DEFAULT_ENCODING
        self.set_filename(None)

        if octave < 0:
            freq = self.frequencies[note] / abs(octave)
        elif octave > 0:
            freq = self.frequencies[note] * abs(octave)
        else:
            freq = self.frequencies[note]
            
        snd = create_sine_wave(int(freq), self.default_amp, s)
        self.set_pygame_sound(snd)
                
        
####################------------------------------------------------------------
## Helper functions
####################------------------------------------------------------------


def load_pygame_sound(filepath):
    '''Return a pygame Sound object from the file at str filepath. If 
    that file is not a .wav or is corrupt in some way raise a TypeError.'''
    
    # Check if the file exists
    if not os.access(filepath, os.F_OK):
        raise Exception("This file does not exist.")
    
    # Check if it is a .wav file
    if sndhdr.what(filepath)[0]:
        assert sndhdr.what(filepath)[0] == 'wav', "The file is not a .wav file"
    
    # Check the compression. Wave_read.getcomptype() will raise an Error if it is
    # compressed.
    wav = wave.open(filepath, 'r')
    try:
        wav.getcomptype()
    except:
        raise TypeError("This .wav file is compressed.")
    wav.close()
    
    return pygame.mixer.Sound(filepath)


def create_pygame_sound(s):
    '''Return a pygame sound object with s number of silent samples.'''

    if DEFAULT_CHANNELS == 1:
        
        # numpy.zeros returns an array object with all 0s in the
        # specified encoding. In sound terms, this is silence.
        sample_array = numpy.zeros(s, AUDIO_ENCODINGS[DEFAULT_ENCODING])
    else:
        sample_array = numpy.zeros((s, 2), AUDIO_ENCODINGS[DEFAULT_ENCODING])
    return sample_array_to_pygame(sample_array)


def create_sine_wave(hz, amp, samp):
    '''Return a pygame sound samp samples long in the form of a sine wave 
    with frequency hz and amplitude amp in the range [0, 32767].'''
    
    # Default frequency is in samples per second
    samples_per_second = float(DEFAULT_SAMP_RATE)
    
    # Hz are periods per second
    seconds_per_period = 1.0 / hz
    samples_per_period = samples_per_second * seconds_per_period
    if DEFAULT_CHANNELS == 1:
        samples = numpy.array(range(samp), 
                              numpy.float)
    else:
        samples = numpy.array([range(samp), range(samp)], 
                              numpy.float)
        samples = samples.transpose()
    
    # For each value in the array multiply it by 2 pi, divide by the 
    # samples per period, take the sin, and multiply the resulting
    # value by the amplitude.
    samples = numpy.sin((samples * 2.0 * math.pi) / samples_per_period) * amp
    
    # Convert the array back into one with the appropriate encoding
    samples = numpy.array(samples, AUDIO_ENCODINGS[DEFAULT_ENCODING])
    return sample_array_to_pygame(samples)


def pygame_to_sample_array(pygame_snd):
    '''Return a numpy array object, which allows direct access to specific
    sample values in the buffer of the pygame.mixer.Sound object pygame_snd.'''
     
    data = pygame_snd.get_buffer()
    
    # Create a numpy array from the buffer with the default encoding
    array = numpy.frombuffer(data, AUDIO_ENCODINGS[DEFAULT_ENCODING])
    
    # If there are two channels make the array object 2D
    if DEFAULT_CHANNELS == 2:
        array.shape = (len(array) / 2, 2)
    return array


def sample_array_to_pygame(samp_array):
    '''Return a new pygame.mixer.Sound object from a numpy array object 
    samp_array. Requires that samp_array is an appropriate 1D or 2D shape.'''

    shape = samp_array.shape
    
    # Check if array has the right shape
    if DEFAULT_CHANNELS == 1:
        if len (shape) != 1:
            raise ValueError("Array must be 1-dimensional for mono sound")
    else:
        if len (shape) != 2:
            raise ValueError("Array must be 2-dimensional for stereo sound")
        elif shape[1] != DEFAULT_CHANNELS:
            raise ValueError("Array depth must match number of sound channels")
    
    return pygame.mixer.Sound(samp_array)

