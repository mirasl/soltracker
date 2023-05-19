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

# Generates a sequence of note durations based on pitches
def generate_sequence(notes : list, dur : float):
	seq = [dur] * len(notes)
	notesIndex = 1
	seqIndex = 1
	while notesIndex < len(notes):
		if notes[notesIndex] == 0:
			seq.pop(seqIndex)
			seq[seqIndex - 1] += dur
		else:
			seqIndex += 1
		notesIndex += 1
	return seq

def to_frequency(pits : list, addend : int):
	for i in range(len(pits)):
		if pits[i] != 0:
			pits[i] = frequencies[pits[i] + addend]
	return pits


s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1, audio="jack").boot()

piano_table = HarmTable([1,0.25,0.1875,0.1,0.09,0.09,0.025,0.015])
cos_table = CosTable()
triangle_table = TriangleTable()

def generate_track(wave_table : PyoTableObject, envelope_table : PyoObject, frequencies : list, 
		base_duration : float, mul : float = 0.1):
	durations = generate_sequence(frequencies, base_duration)
	frequencies = [i for i in frequencies if i != 0]

	sequence = Seq(seq=durations).play()

	this_pitch = Iter(sequence.mix(1), choice=frequencies)
	this_duration = Iter(sequence.mix(1), choice=durations)

	envelope = TrigEnv(sequence, table=envelope_table, dur=this_duration, mul=mul)

	osc = Osc(table=wave_table, freq=this_pitch, mul=envelope).out()

	return osc




# class track:
# 	def __init__(self, table : PyoTableObject, envelope : PyoObject, frequencies : list):
# 		durations = generate_sequence(frequencies, 0.125)
# 		self.frequencies = [i for i in frequencies if i != 0]

# 		sequence = Seq(seq=durations).Play()
		
# 		this_frequency = Iter(sequence.mix(1), choice=frequencies)
# 		this_duration = Iter(sequence.mix(1), choice=durations)
# 		self.osc = Osc(table=table, freq=this_frequency, mul=envolope)

piano_envelope = CosTable([(0,0),(50,1),(4000,.5),(8192,0)])
spizazz_envelope = LinTable([(0,0),(10,1),(8000,0.1),(8192,0)])

piano_track = generate_track(
	wave_table=piano_table, 
	envelope_table=piano_envelope, 
	frequencies=to_frequency([3, 0, 5, 6, 0, 8, 3, 5, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 57), 
	base_duration=0.07 * 4/3,
	mul=0.35
)
triangle_track = generate_track(
	wave_table=triangle_table, 
	envelope_table=CosTable([(0,0),(25,1),(4000,.5),(1892,0)]), 
	frequencies=to_frequency([3, 8, 1, 0], 50 - 24),
	base_duration=0.56, 
	mul=0.6
)
spizazz_track1 = generate_track(
	wave_table=CosTable(),
	envelope_table=spizazz_envelope,
	frequencies=to_frequency([6,6,5,0], 50),
	base_duration=0.56
)
spizazz_track2 = generate_track(
	wave_table=CosTable(),
	envelope_table=spizazz_envelope,
	frequencies=to_frequency([13,12,12,0], 50),
	base_duration=0.56
)
spizazz_track3 = generate_track(
	wave_table=CosTable(),
	envelope_table=spizazz_envelope,
	frequencies=to_frequency([17,16,15,0], 50),
	base_duration=0.56
)
spizazz_track4 = generate_track(
	wave_table=CosTable(),
	envelope_table=spizazz_envelope,
	frequencies=to_frequency([22,21,20,0], 50),
	base_duration=0.56
)
# rand_list = [random.uniform(0,1) for i in range(100)]
# percussion_track = generate_track(
# 	wave_table=CosTable([(0,1),(8191,1)]),
# 	envelope_table=spizazz_envelope,
# 	frequencies=to_frequency([6,0,0,6,0,6,6,0,0,6,0,6,6,0,0,6,0,6,6,0,6,24,12,1],50),
# 	base_duration=0.28/3,
# 	mul=0.5
# )
ladida_track = generate_track(
	wave_table=HannTable(),
	envelope_table=spizazz_envelope,
	frequencies=to_frequency([3,0,5,6,0,3,8,0,10,12,0,15,13,0,8,5,0,1,5,0,6,8,5,1],50 + 12),
	base_duration=0.28/3,
	mul=0.35
)

# for table in instrument_tables:
# 	# Pitch as a list:
# 	pitches = ToFrequency([1, 1, 13, 0, 8, 0, 0, 7, 0, 6, 0, 4, 0, 1, 4, 6], 50)
# 	# Generate durations in a sequence based upon pitches:
# 	durations = generate_sequence(pitches, 0.125)
# 	# Remove zeroes from pits:
# 	pitches = [i for i in pitches if i != 0]


# 	envelope_table = CosTable([(0,0),(50,1),(4000,.5),(8192,0)])

# 	sequence = Seq(seq=durations).play()

# 	this_pitch = Iter(sequence.mix(1), choice=pitches)
# 	this_duration = Iter(sequence.mix(1), choice=durations)

# 	envolope = TrigEnv(sequence, table=envelope_table, dur=this_duration, mul=.3)

# 	osc = Osc(table=table, freq=this_pitch, mul=envolope).out()

# 	scope = Scope(osc)

s.gui(locals())


# Basic stuff:
# 	Each instrument has a
# 		- Table (of harmonics)
# 		- Envelope
#
#	A track contains
#		- Instrument
#		- Pitches
# More:
# 	Modifiers
# 		- Pitch bend
# 		- Vibrato
# 		- Volume
# 		- Note length (rest vs hold)
