from media import *
from math import *

A0 = 27.5000
AS0 = 29.1352
B0 = 30.8677
C1 = 32.7032
CS1 = 34.6478
D1 = 36.7081
DS1 = 38.8909
E1 = 41.2034
F1 = 43.6535
FS1 = 46.2493
G1 = 48.9994
GS1 = 51.9131
A1 = 55.0000
AS1 = 58.2705
B1 = 61.7354
C2 = 65.4064
CS2 = 69.2957
D2 = 73.4162
DS2 = 77.7817
E2 = 82.4069
F2 = 87.3071
FS2 = 92.4986
G2 = 97.9989
GS2 = 103.8262
A2 = 110.0000
AS2 = 116.5409
B2 = 123.4708
C3 = 130.8128
CS3 = 138.5913
D3 = 146.8324
DS3 = 155.5635
E3 = 164.8138
F3 = 174.6141
FS3 = 184.9972
G3 = 195.9977
GS3 = 207.6523
A3 = 220.0000
AS3 = 233.0819
B3 = 246.9417
C4 = 261.6256
CS4 = 277.1826
D4 = 293.6648
DS4 = 311.1270
E4 = 329.6276
F4 = 349.2282
FS4 = 369.9944
G4 = 391.9954
GS4 = 415.3047
A4 = 440.0000
AS4 = 466.1638
B4 = 493.8833
C5 = 523.2511
CS5 = 554.3653
D5 = 587.3295
DS5 = 622.2540
E5 = 659.2551
F5 = 698.4565
FS5 = 739.9888
G5 = 783.9909
GS5 = 830.6094
A5 = 880.0000
AS5 = 932.3275
B5 = 987.7666
C6 = 1046.5023
CS6 = 1108.7305
D6 = 1174.6591
DS6 = 1244.5079
E6 = 1318.5102
F6 = 1396.9129
FS6 = 1479.9777
G6 = 1567.9817
GS6 = 1661.2188
A6 = 1760.0000
AS6 = 1864.6550
B6 = 1975.5332
C7 = 2093.0045
CS7 = 2217.4610
D7 = 2349.3181
DS7 = 2489.0159
E7 = 2637.0205
F7 = 2793.8259
FS7 = 2959.9554
G7 = 3135.9635
GS7 = 3322.4376
A7 = 3520.0000
AS7 = 3729.3101
B7 = 3951.0664
C8 = 4186.0090

def playNote(freq, duration):
    """play a note of freq (hertz) for duration (seconds)"""
    snd = Sound();
    snd.makeEmptyLength(duration)
    
    rate = snd.getSamplingRate()
    notef = rate/freq;
   
    for i in range(1,snd.getLength()):        
        value = 2000* sin(i*2*pi/notef)        
        snd.setSampleValue(i, int(value))
    
    snd.blockingPlay()
    return snd


def playValk():
    playNote(B4, 0.2)
    playNote(F4, 0.1)
    playNote(B4, 0.1)
    playNote(D5, 0.3)
    playNote(B4, 0.3)
    
    playNote(D5, 0.2)
    playNote(B4, 0.1)
    playNote(D5, 0.1)
    playNote(F5, 0.3)
    playNote(D5, 0.3)
    
    playNote(F5, 0.2)
    playNote(D5, 0.1)
    playNote(F5, 0.1)
    playNote(A5, 0.3)
    playNote(A4, 0.3)
    
    playNote(D5, 0.2)
    playNote(A4, 0.1)
    playNote(D5, 0.1)
    playNote(F5, 0.5)


