from pyo import *
import random

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

# parses string of solfege and returns array of midi pitches
def parse_solfege(solfege_string : str):
	pitches = []
	word = ""

	for char in solfege_string:
		if char == ' ':
			if word[0] == '^':
				pitches.append(solfege[word[1:]])
				pitches[len(pitches) - 1] += 12
			elif word[0] == '/':
				pitches.append(solfege[word[1:]])
				pitches[len(pitches) - 1] -= 12
			elif word[0] == '-':
				pitches.append(None)
			else:
				pitches.append(solfege[word])
			word = ""
		else:
			word += char
	
	return pitches

# Changes midi pitches to piano frequencies
def to_frequency(pits : list, addend : int = 50):
	for i in range(len(pits)):
		if pits[i] != None:
			pits[i] = frequencies[pits[i] + addend]
	return pits

# "solfege to hertz" (nonverbose helper method)
def s2h(solfege_string : str, addend : int = 50):
	return to_frequency(parse_solfege(solfege_string), addend)

# Generates a sequence of note durations based on pitches
def generate_sequence(notes : list, dur : float):
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


# Generates a track and plays it asynchronously
def generate_track(wave_table : PyoTableObject, envelope_table : PyoTableObject, frequencies : list, 
		base_duration : float, mul : float = 0.1, feedback : float = 0.0):
	durations = generate_sequence(frequencies, base_duration)
	frequencies = [i for i in frequencies if i != None]

	sequence = Seq(seq=durations).play()

	this_pitch = Iter(sequence.mix(1), choice=frequencies)
	this_duration = Iter(sequence.mix(1), choice=durations)

	envelope = TrigEnv(sequence, table=envelope_table, dur=this_duration, mul=mul)

	osc = OscLoop(table=wave_table, freq=this_pitch, mul=envelope, feedback=feedback).out()

	return osc

def generate_noise_track(pattern : list, base_duration : float, envelope_table : PyoTableObject, 
		mul : float = 0.1):
	durations = generate_sequence(pattern, base_duration)
	sequence = Seq(seq=durations).play()
	this_duration = Iter(sequence.mix(1), choice=durations)

	envelope = TrigEnv(sequence, table=envelope_table, dur=this_duration, mul=mul)
	noise = Noise(mul=envelope).out()

	return noise

# Basic stuff:
# 	Each instrument has a
# 		- Table (of harmonics)
# 		- Envelope
#
#	A track contains
#		- Instrument
#		- Pitches
#		- Automation channels
#
# More:
# 	Modifiers
# 		- Pitch bend
# 		- Vibrato
# 		- Volume
# 		- Note length (rest vs hold)
#		- EQ shift over time
#		- Tone shift over time
#		- Microtonal pitches
#		- Panning
