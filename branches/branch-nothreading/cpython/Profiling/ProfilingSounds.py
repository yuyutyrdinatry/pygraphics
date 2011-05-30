import cProfile
from media import *

tests = 1000

def test_load_sound():
    print "Testing load_sound"
    for i in range(1, tests):
        sound = load_sound("resources/sounds/blip.wav")
        
def test_create_sound():
    print "Testing create_sound"
    for i in range(1, tests):
        new_sound = create_sound(5)
        
def test_create_note():
    print "Testing create_note"
    for i in range(1, tests):
        new_note = create_note('C', 5)
        
def test_get_samples():
    print "Testing get_samples"
    sound = create_sound(10)
    for i in range(1, tests):
        sample_list = get_samples(sound)
        
def test_get_max_sample():
    print "Testing get_max_sample"
    sound = load_sound("resources/sounds/blip.wav")
    for i in range(1, tests):
        max_sample = get_max_sample(sound)
        
def test_get_min_sample():
    print "Testing get_min_sample"
    sound = load_sound("resources/sounds/blip.wav")
    for i in range(1, tests):
        min_sample = get_min_sample(sound)
        
def test_concatenate():
    print "Testing concatenate"
    sound1 = load_sound("resources/sounds/blip.wav")
    sound2 = load_sound("resources/sounds/blip.wav")
    for i in range(1, tests):
        sound3 = concatenate(sound1, sound2)
        
def test_append_silence():
    print "Testing append_silence"
    sound = load_sound("resources/sounds/blip.wav")
    for i in range(1, tests):
        sound2 = append_silence(sound, 5)
        
def test_crop_sound():
    print "Testing crop_sound"
    sound = load_sound("resources/sounds/preamble.wav")
    for i in range(1, tests):
        sound2 = crop_sound(sound, 1, 3)

def test_insert():
    print "Testing insert"
    sound1 = load_sound("resources/sounds/preamble.wav")
    sound2 = load_sound("resources/sounds/blip.wav")
    for i in range(1, tests):
        sound3 = insert(sound1, sound2, 2)
        
def test_play():
    print "Testing play"
    sound = load_sound("resources/sounds/blip.wav")
    for i in range(1, 10):
        play(sound)
        
def test_play_in_range():
    print "Testing play_in_range"
    sound = load_sound("resources/sounds/preamble.wav")
    for i in range(1, 10):
        play_in_range(sound, 1, 3)
        
def test_stop():
    print "Testing stop"
    sound = load_sound("resources/sounds/preamble.wav")
    for i in range(1, 10):
        play(sound)
        stop(sound)
        
def test_get_sampling_rate():
    print "Testing get_sampling_rate"
    sound = load_sound("resources/sounds/preamble.wav")
    for i in range(1, tests):
        rate = get_sampling_rate(sound)
        
def test_get_sample():
    print "Testing get_sample"
    sound = load_sound("resources/sounds/preamble.wav")
    for i in range(1, tests):
        sample = get_sample(sound, 5)
        
def test_get_waveform():
    print "Testing get_waveform"
    sound = load_sound("resources/sounds/preamble.wav")
    for i in range(1, tests):
        wave = get_waveform(sound)
        
def run_profiling_tests_sound():
    cProfile.run("test_load_sound()")
    cProfile.run("test_create_sound()")
    cProfile.run("test_create_note()")
    cProfile.run("test_get_samples()")
    cProfile.run("test_get_max_sample()")
    cProfile.run("test_get_min_sample()")
    cProfile.run("test_concatenate()")
    cProfile.run("test_append_silence()")
#    cProfile.run("test_crop_sound()")
    cProfile.run("test_insert()")
    cProfile.run("test_play()")
    cProfile.run("test_play_in_range()")
    cProfile.run("test_stop()")
    cProfile.run("test_get_sampling_rate()")
    cProfile.run("test_get_sample()")
    cProfile.run("test_get_waveform()")
    
    
#run_profiling_tests_sound()
# Tests for sampling functions still need to be written.