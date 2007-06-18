import unittest
import os.path
from TestExecute import *
from media import *
import random

# we MUST set the debug level to 1 to force errors to return
debugLevel = 1

def soundEqualsSound(sound, other):
	# helper function to compare sound sample values
	if sound.getLength() != other.getLength():
		print 'difflen'
		return False
	for idx in range(1, sound.getLength()+1):
		if (sound.getSampleValue(idx) != other.getSampleValue(idx)):
			print 'diffval'
			return False
	return True

class Test_Sound(unittest.TestCase):
	''' Tests the media.py Sound class members '''
			
	def tearDown(self):
		# delete the sound after use
		try:
			del self.sound
		except:
			done = TRUE # 			
		
	def testConstructor(self):
		# test that calls to sound constructor
		try:
			self.sound = Sound(ress('flip.wav'))
			self.sound = Sound('flip.wav')			
			self.sound = Sound('')
		except (StandardError, IOError), e: 
			#expected to fail
			pass
		except e:
			self.fail('Unknown error encountered ' + str(e))
		# normal calls
		self.sound = Sound(ress('blip.wav'))
		del self.sound
		self.sound = Sound(ress('preamble.wav'))
		del self.sound
		self.sound = Sound(None)
		
	def testMakeEmptyLength(self):
		global defaultFrequency
		# test the creation of a new empty sound
		self.sound = Sound(None)		
		# fail on negative lengths
		self.assertRaises(ValueError, self.sound.makeEmptyLength, -1)
		self.assertRaises(ValueError, self.sound.makeEmptyLength, -999)		
		del self.sound
		# normal lengths
		lengths = (0, 1, 60)
		for len in lengths:
			self.sound = Sound(None)
			self.sound.makeEmptyLength(len) 
			self.assertEqual(self.sound.getLength(), len*defaultFrequency, 'Invalid sound lengths (' + str(len) + ')')
			del self.sound
			
	def testPlayInRangeAndBlocking(self):
		# can't actually play test that a sound is played during unit tests, so just
		# check that it fails on incorrect input
		# length of blip.wav: 20468
				
		len = 20468
		self.sound = Sound(ress('blip.wav'))
		# test both the blocking and non-blocking versions of this	
		a = self.sound.blockingPlayInRange
		funcs = (self.sound.playInRange, self.sound.blockingPlayInRange)
		for playFunc in funcs:
			self.assertRaises(ValueError, playFunc, 0, 0) 	# start = 0
			self.assertRaises(ValueError, playFunc, 0, len)	# start = 0
			self.assertRaises(ValueError, playFunc, 1, len+1)	# end > len
			self.assertRaises(ValueError, playFunc, 1, 0)	# start > end, invalid end
			self.assertRaises(ValueError, playFunc, 2, 1)	# start > end, 
			self.assertRaises(ValueError, playFunc, 0, 0)	# same
			self.assertRaises(ValueError, playFunc, 1, 1)	# same
			self.assertRaises(ValueError, playFunc, len-1, len-1)	# same
		
	def testGetLength(self):
		# ensure that the correct length is returned (partially tested above)
		# these calls will fail
		failSounds = (Sound(None),)
		for failSound in failSounds:			
			self.assertRaises(ValueError, failSound.makeEmptyLength, -1)			
		
			
	def testSetGetSampleValueAndObject(self):
		# test empty sound
		self.sound = Sound(None)
		self.sound.makeEmptyLength(1)
		# test that each sample is zero
		for idx in range(1, self.sound.getLength()+1):
			self.assertEqual(self.sound.getSampleValue(idx), 0, 'Samples not equal')
		# TODO: try on a loaded sound (need a simple sound)
		# fail cases (get)
		self.assertRaises(ValueError, self.sound.getSampleValue, -10)
		self.assertRaises(ValueError, self.sound.getSampleValue, 0)
		self.assertRaises(ValueError, self.sound.getSampleValue, self.sound.getLength()+1)
		# fail cases (get object)
		self.assertRaises(ValueError, self.sound.getSampleObjectAt, -10)
		self.assertRaises(ValueError, self.sound.getSampleObjectAt, 0)
		self.assertRaises(ValueError, self.sound.getSampleObjectAt, self.sound.getLength()+1)
		# fail cases (set)
		self.assertRaises(ValueError, self.sound.setSampleValue, -10, 0)
		self.assertRaises(ValueError, self.sound.setSampleValue, 0, 0)
		self.assertRaises(ValueError, self.sound.setSampleValue, self.sound.getLength()+1, 0)
		# sample value must be integer
		self.assertRaises(ValueError, self.sound.setSampleValue, 1, 1000.3) 
		
		# why would you want to do this? If this is checked, then all indicies must
		# be checked for value valid int values. Better to let the system pop up the message.		
		# self.assertRaises(ValueError, self.sound.setSampleValue, 1, "asdf")
		# test setting and getting of indices and values
		# TODO: what are values bounded by? anything?
		len = 100
		indices = random.sample(range(1,self.sound.getLength()), len)
		values = random.sample(range(0,100), len)
		for idx in range(0,len):
			self.sound.setSampleValue(indices[idx], values[idx])
			self.assertEqual(self.sound.getSampleValue(indices[idx]), values[idx], 'Improper sample value set')
		
	def testGetSamplingRate(self):
		# ensure that the global freq is the same as that for the sound
		global defaultFrequency
		self.sound = Sound(None)
		self.assertEqual(self.sound.getSamplingRate(), defaultFrequency, 'Improper sound sampling rate')
		
	def testWriteTo(self):
		# ensure that the sound files are being written correctly
		# load and save the file ensuring all the samples have the same values
		input = ('blip.wav', 'preamble.wav')
		output = ('blip.tmp.wav', 'preamble.tmp.wav')
		self.failUnless(len(input) == len(output), 'Test arrays are mapped 1:1')
		
		for idx in range(len(input)):
			self.sound = Sound(ress(input[idx]))
			self.sound.writeTo(ress(output[idx]))
			# load the outputed array
			newSound = Sound(ress(output[idx]))
			self.failUnless(soundEqualsSound(self.sound, newSound), 'Sounds do not match (' + input[idx] + ')')
			del self.sound, newSound
		# test on empty sound
		emptyName = 'emptySound.tmp.wav'
		self.sound = Sound(None)
		self.sound.makeEmptyLength(4)
		self.sound.writeTo(ress(emptyName))
		# load the outputed array
		newSound = Sound(ress(emptyName))
		self.failUnless(soundEqualsSound(self.sound, newSound), 'Sounds do not match (' + input[idx] + ')')
		
class Test_Sound_Helpers(unittest.TestCase):
	''' Tests global functions related to the Sound class '''
	
	def testMakeSound(self):
		# ensure that the sound made is the same as that done the manual way
		self.assertRaises(ValueError, makeSound, ress('bllip.wav'))
		self.assertRaises(ValueError, makeSound, 'bllip.wav')
		snd = makeSound(ress('blip.wav'))
		sndMan = Sound(ress('blip.wav'))
		self.failUnless(soundEqualsSound(snd, sndMan), 'Sounds do not match')
		
	def testMakeEmptySound(self):
		# ensure that the sound made is the same as that done the manual way
		snd = makeEmptySound(1)
		sndMan = Sound()
		sndMan.makeEmptyLength(1)
		self.failUnless(soundEqualsSound(snd, sndMan), 'Sounds do not match')
						
	def testNonSoundObjectCall(self):
		# ensuring that all the picture global convenience functions fail on non-Sound objects
		self.assertRaises(ValueError, getSamples, DummyClass())
		self.assertRaises(ValueError, play, DummyClass())
		self.assertRaises(ValueError, blockingPlay, DummyClass())
		self.assertRaises(ValueError, playInRange, DummyClass(), 0, 0)
		self.assertRaises(ValueError, blockingPlayInRange, DummyClass(), 0, 0)
		self.assertRaises(ValueError, getSamplingRate, DummyClass())
		self.assertRaises(ValueError, setSampleValueAt, DummyClass(), 0, 0)
		self.assertRaises(ValueError, getSampleValueAt, DummyClass(), 0)
		self.assertRaises(ValueError, getSampleObjectAt, DummyClass(), 0)
		self.assertRaises(ValueError, getLength, DummyClass())
		self.assertRaises(ValueError, writeSoundTo, DummyClass(), None)
		