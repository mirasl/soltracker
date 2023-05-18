from pyo import *

# i.e. [0.125, 0.125, 0.25, 0.125, 0.5, ...etc...]
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

s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1, audio="jack").boot()

# Pitch and duration data
pits = [1, 1, 13, 0, 8, 0, 0, 7, 0, 6, 0, 4, 0, 1, 4, 6]
for i in range(len(pits)):
	if pits[i] != 0:
		pits[i] = frequencies[pits[i] + 60]
time_seq = generate_sequence(pits, 0.125)
pits = [i for i in pits if i != 0]
print(time_seq)
# Duration / time to give the integer sequence to Seq object


# Amplitude envelope
env = CosTable([(0,0),(100,1),(500,.5),(8192,0)])

# trigger sequence base on duration sequence
seq = Seq(seq=time_seq).play()
# get pitch and duration from lists (.mix(1) to avoid duplication)
pit = Iter(seq.mix(1), choice=pits)
ones = Iter(seq.mix(1), choice=[1.0])

dur = Iter(seq.mix(1), choice=time_seq)
# trig the amplitude envelope (no mix to keep the polyphony and not truncate an envelope)
amp = TrigEnv(seq, table=env, dur=dur, mul=.3)
# output
osc = SineLoop(freq=pit, feedback=.07, mul=amp).out() #(pit / 2*abs(pit)) + 0.5

s.gui(locals())




# version not using triggers: #####################################################################
# from pyo import *

# frequencies = [
# 	16.35, 	17.32, 	18.35, 	19.45, 	20.60, 	21.83, 	23.12, 	24.50, 	25.96, 	27.50, 	29.14, 	30.87,
# 	32.70, 	34.65, 	36.71, 	38.89, 	41.20, 	43.65, 	46.25, 	49.00, 	51.91, 	55.00, 	58.27, 	61.74,
# 	65.41, 	69.30, 	73.42, 	77.78, 	82.41, 	87.31, 	92.50, 	98.00, 	103.83, 110.00, 116.54, 123.47,
# 	130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94,
# 	261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88,
# 	523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77,
# 	1046.50,1108.63,1174.66,1244.51,1318.51,1396.91,1479.98,1567.98,1661.22,1760.00,1864.66,1975.53,
# 	2093.00,2217.46,2349.32,2489.02,2637.02,2793.83,2959.96,3135.96,3322.44,3520.00,3729.31,3951.07,
# 	4186.01,4434.92,4698.63,4978.03,5274.04,5587.65,5919.91,6271.93,6644.88,7040.00,7458.62,7902.13
# ]

# s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1, audio="jack").boot()

# # Pitch and duration data
# pits = [5, 0, 5, 0, 6, 0, 8, 0, 8, 0, 6, 0, 5, 0, 3, 0, 1, 0, 1, 0, 3, 0, 5, 0, 5, 0, 0, 3, 3, 0, 0, 0]
# for i in range(len(pits)):
# 	if pits[i] != 0:
# 		pits[i] = frequencies[pits[i] + 60]
# durs = [.125]

# # start of the note is the sum of previous duration
# offset = 0
# # list to store audio objects
# objs = []
# osc = None
# for i in range(32):
# 	pit = pits[i]
# 	dur = durs[0]

# 	start = offset
# 	offset = start + dur

# 	amp = Fader(fadein=0.005, fadeout=dur-0.005, dur=dur, mul=.3).play(delay=start, dur=dur+.1)
	
# 	osc = SineLoop(freq=pit, feedback=.07, mul=amp).out(delay=start, dur=dur+.1)

# 	objs.append(amp)
# 	objs.append(osc)
# 	scope=Scope(osc)

# print(objs)

# scope = Scope(osc)

# s.gui(locals())
