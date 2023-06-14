from pyo import *
import random
	# import wx

	# app = wx.App()
	# frame = wx.Frame(None, title="Hello World")
	# frame.Show()
	# slider = PyoGuiControlSlider(parent=frame, minvalue=0,maxvalue=1)
	# slider.Show()
	# # app.MainLoop()
class Soltracker:
	s = Server(duplex=0).boot()

	spb = 0

	def __init__(self, bpm) -> None:
		self.spb = 60 / bpm
	
	print(spb)
	
	#s = Server(sr=44100, nchnls=2, buffersize=512, duplex=2, audio='jack').boot()

	frequencies = [
		16.35, 	17.32, 	18.35, 	19.45, 	20.60, 	21.83, 	23.12, 	24.50, 	25.96, 	27.50, 	29.14, 	30.87,
		32.70, 	34.65, 	36.71, 	38.89, 	41.20, 	43.65, 	46.25, 	49.00, 	51.91, 	55.00, 	58.27, 	61.74,
		65.41, 	69.30, 	73.42, 	77.78, 	82.41, 	87.31, 	92.50, 	98.00, 	103.83, 110.00, 116.54, 123.47,
		130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94,
		261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88,
		523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77,
		1046.50,1108.63,1174.66,1244.51,1318.51,1396.91,1479.98,1567.98,1661.22,1760.00,1864.66,1975.53,
		2093.00,2217.46,2349.32,2489.02,2637.02,2793.83,2959.96,3135.96,3322.44,3520.00,3729.31,3951.07,
		4186.01,4434.92,4698.63,4978.03,5274.04,5587.65,5919.91,6271.93,6644.88,7040.00,7458.62,7902.13
	]

	solfege = {
		"0" : -111,
		"do" : 1,
		"di" : 2,
		"ra" : 2,
		"re" : 3,
		"ri" : 4,
		"me" : 4,
		"mi" : 5,
		"fa" : 6,
		"fi" : 7,
		"se" : 7,
		"so" : 8,
		"sol" : 8,
		"si" : 9,
		"le" : 9,
		"la" : 10,
		"li" : 11,
		"te" : 11,
		"ti" : 12,
	}

	tone_library = {
		"piano" : HarmTable([1,0.25,0.1875,0.1,0.09,0.09,0.025,0.015]),
		"plink-mallets" : HarmTable([1,0,-1,0,1,0,-1]),
		"oomph" : HarmTable([1,0.2,-0.2,-0.2,0.2])
	}

	envelope_library = {
		"spizazz" : LinTable([(0,0),(10,1),(8000,0.3),(8192,0)]),
		"piano" : CosTable([(0,0),(50,1),(4000,.5),(8192,0)])
	}

	def set_bpm(new_bpm):
		bpm = new_bpm
		spb = 60 / new_bpm

	# parses string of solfege and returns array of midi pitches
	def parse_solfege(self, solfege_string : str):
		pitches = []
		word = ""

		for char in solfege_string:
			if char == ' ':
				if word[0] == '^':
					pitches.append(self.solfege[word[1:]])
					pitches[len(pitches) - 1] += 12
				elif word[0] == '/':
					pitches.append(self.solfege[word[1:]])
					pitches[len(pitches) - 1] -= 12
				elif word[0] == '-':
					pitches.append(None)
				else:
					pitches.append(self.solfege[word])
				word = ""
			else:
				word += char
		
		return pitches

	# Changes midi pitches to piano frequencies
	def to_frequency(self, pits : list, addend : int = 50, modSignal : PyoObject = Linseg([(0,1)]).play()):
		for i in range(len(pits)):
			if pits[i] == -111:
				pits[i] = 0
			elif pits[i] != None:
				pits[i] = self.frequencies[pits[i] + addend] * modSignal
		return pits

	# "solfege to hertz" (nonverbose helper method)
	def s2h(self, solfege_string : str, addend : int = 50, modSignal : PyoObject = Linseg([(0,1)]).play()):
		return self.to_frequency(self.parse_solfege(solfege_string), addend, modSignal)

	# Generates a sequence of note durations based on pitches
	def generate_sequence(self, notes : list, dur : float):
		seq = [dur] * len(notes)
		notesIndex = 1
		seqIndex = 1
		while notesIndex < len(notes):
			if notes[notesIndex] == None:
				seq.pop(seqIndex)
				seq[seqIndex - 1] += dur
			else:
				seqIndex += 1
			notesIndex += 1
		return seq

	# Generates a track and plays it asynchronously, returns 2-index list of osc for each channel (left
	# and right, respectively)
	def generate_track(self, wave_table : PyoTableObject, envelope_table : PyoTableObject, frequencies : list, 
			div : float, mul : float = 0.1, feedback : float = 0.0):
		durations = self.generate_sequence(frequencies, self.spb/div)
		frequencies = [i for i in frequencies if i != None]

		sequence = Seq(seq=durations).play()

		this_pitch = Iter(sequence.mix(1), choice=frequencies)
		this_duration = Iter(sequence.mix(1), choice=durations)

		envelope = TrigEnv(sequence, table=envelope_table, dur=this_duration, mul=mul)

		osc = OscLoop(table=[wave_table, wave_table], freq=this_pitch, mul=envelope, feedback=feedback)
		#oscRight = OscLoop(table=wave_table, freq=this_pitch, mul=envelope, feedback=feedback)

		return osc

	# generates a noise (static) track and plays it asynchronously, returns 2-index list of osc for 
	# each channel (left and right, respectively)
	def generate_noise_track(self, pattern : list, div : float, envelope_table : PyoTableObject, 
			mul : float = 0.1):
		durations = self.generate_sequence(pattern, self.spb/div)
		sequence = Seq(seq=durations).play()
		this_duration = Iter(sequence.mix(1), choice=durations)

		envelope = TrigEnv(sequence, table=envelope_table, dur=this_duration, mul=mul)

		noise = Noise(mul=[envelope, envelope])

		return noise

	# generates multiple tracks and plays them all asynchronously
	def generate_chord_track(self, wave_table : PyoTableObject, envelope_table : PyoTableObject, 
			frequency_list : list, div : float, mul : float = 0.1, feedback : float = 0.0):
		tracks = []
		for frequencies in frequency_list:
			tracks.append(self.generate_track(wave_table, envelope_table, frequencies,
					div, mul, feedback))
		# tracks = self.generate_noise_track(wave_table, envelope_table, frequency_list, div, mul, feedback)
		return tracks

	"""
	Basic stuff:
		Each instrument has a
			- Table (of harmonics)
			- Envelope

		A track contains
			- Instrument
			- Pitches
			- Automation channels (bus to them??)

	More:
		Modifiers (ordered roughly from most to least important)
			- Volume
				control mul with sequence
			- Panning
				???
			- Note length (rest vs hold)
				???
			- Vibrato
				??? apply an oscillator and feed that into frequency
			- Pitch bend
				??? interpolate between frequencies
			- EQ shift over time
				maybe combine with volume???
			- Tempo
				??? this is tough because dur is calculated at beginning
			- Microtonal pitches
				???
			- Tone shift over time
				???

	Workflow:
		Create a new track
			- Create a wave table
			- Create an envelope table
			- Input frequency list
			- Input other info (max volume, base duration, etc) as necessary
		Create a channel
			- Select type (pitch bend, vibrato, volume, etc)
			- Input channel list
		Bus to channels
			- Link a track to a channel

	OVERALL:
	- Header (bpm and stuff)
	- Tracks (instruments and their notes/frequencies)
	- Channels (gradual modifiers)
	- Buses (link tracks to channels)

	ALTERNATE PLAN:
	- Create header
		- bpm
	- Create tracks
		- Wavetables
	- Create automation components
		- Pitch
			table of frequencies
			??? also include note length vs rest ???

		- Envelope DONE
			standard ADSR table

		- MacroDynamics DONE
			control signal representing max volume over time

		- Pan DONE
			control signal representing percentage, from 0.0 to 1.0, of the signal gotten by the LEFT
			channel. Ex. 0.5 => even panning, 0.3 => mostly right, 1.0 => completely left
		
		- PitchModulation DONE
			control signal representing frequency scaling of given note. Can be used for PITCH
			BENDS, or for MICROTONAL pitches
			Multiplied by frequency (value of 1 results in normal sound)
			Can also achieve PITCH VIBRATO by applying an LFO, should find an easy way to do this.
	
	- Create master
		- specifies the order of tracks and when to play them

		

	- Link automation components to tracks
	"""