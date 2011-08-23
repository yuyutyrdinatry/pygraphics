#
#  soundlab.py
#  
#
#  Created by Christopher Maddison on 03/07/08.
#  Copyright (c) 2008. All rights reserved.
#

from media import *
import math

mystery = "CCGGAA2GFFEEDD2CGGFFEEDGGFFEEDCCGGAA2GFFEEDD2C"

def create_note(freq, amp, samp):
	'''Return a Sound with frequency freq (in Hz), an amplitude of amp,
	and samp number of samples.'''
	
	snd = create_sound(samp)
	sampling_rate = get_sampling_rate(snd)
	period = 1.0 / freq
	samples_per_cycle = sampling_rate * period
	
	i = 0
	while i < samp:
		val = math.sin( (2 * math.pi * i) / samples_per_cycle ) * amp
		sample = get_sample(snd, i)
		set_values(sample, val, val)
		i += 1
	
	return snd
		
C = create_note(264, 6000, 11025)
D = create_note(297, 6000, 11025)
E = create_note(330, 6000, 11025)
F = create_note(352, 6000, 11025)
G = create_note(396, 6000, 11025)
A = create_note(440, 6000, 11025)
B = create_note(496, 6000, 11025)

def get_note(char):

	if char == "C":
		note = C
	elif char == "D":
		note = D
	elif char == "E":
		note = E
	elif char == "F":
		note = F
	elif char == "G":
		note = G
	elif char == "A":
		note = A
	elif char == "B":
		note = B
	
	return note

def string_to_sound(s):
	
	snd = create_sound(11025)
	i = 0
	while i < len(s):
		if s[i].isdigit():
			count = int(s[i])
			i += 1
			while count > 0:
				snd = concatenate(snd, get_note(s[i]))
				count -= 1
		else:
			snd = concatenate(snd, get_note(s[i]))
		append_silence(snd, 11025 / 5)
		i += 1
	
	return snd
	
def echo(snd, delay):
	
	target = copy(snd)
	source = copy(snd)
	i = delay
	while i < len(target):
		source_sample = get_sample(source, i - delay)
		target_sample = get_sample(target, i)
		l_value = get_left(source_sample) * 0.3 + get_left(target_sample)
		r_value = get_right(source_sample) * 0.3 + get_right(target_sample)
		set_values(target_sample, int(l_value), int(r_value))
		i += 1
		
	return target