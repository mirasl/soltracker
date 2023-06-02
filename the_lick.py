from soltracker import *

# s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1, audio="jack").boot()

sol = Soltracker(214)

# wavetable:
piano_table = sol.tone_library["piano"]
cos_table = CosTable()
triangle_table = TriangleTable()

# envelope:
piano_envelope = sol.envelope_library["piano"]
spizazz_envelope = sol.envelope_library["spizazz"]

# macro volume: (a control signal which directly feeds into mul)
thump_volume = Linseg([(0,0.00), (0.14/3,0.5), (0.56/3,0.6)], loop=True).play()

# pan: (a control signal which represents the percentage of panning recieved by LEFT channel)
dizzy_pan = Linseg([(0,0), (0.56, 1)], loop=True).play()

piano_track = sol.generate_track(
	wave_table=sol.tone_library["piano"], 
	envelope_table=spizazz_envelope, 
	frequencies=sol.s2h("la - ti ^do - ^re la ti - so - la - - - - - - - - - - - - ", 50), 
	div=3,
	mul=0.25
)
# lfo1 = Sine(freq=.1, mul=500, add=1000)
# lfo2 = Sine(freq=.4).range(2, 8)
# bandpass = ButBP(piano_track[0], freq=lfo1).out()
bass_track = sol.generate_track(
	wave_table=triangle_table, 
	envelope_table=CosTable([(0,0),(25,1),(4000,.5),(1892,0)]), 
	frequencies=sol.s2h("re so do - ", 50 - 24),
	div=0.5, 
	mul=0.4
)
spizazz_track = sol.generate_chord_track(
	wave_table=CosTable(),
	envelope_table=spizazz_envelope,
	frequency_list=[
		sol.s2h("fa fa mi - ", 50),
		sol.s2h("^do ti ti - ", 50),
		sol.s2h("^mi ^mi ^re - ", 50),
		sol.s2h("^la ^le ^so - ", 50),
	],
	div=0.5,
	mul=[thump_volume*dizzy_pan, thump_volume*(1-dizzy_pan)]
)
percussion_track = sol.generate_noise_track(
	pattern=sol.parse_solfege("fi - - fi - fi fi - - fi - fi fi - - fi - fi fi - fi ^fi ^do do "),
	div=3,
	envelope_table=spizazz_envelope
)
ladida_track = sol.generate_track(
	wave_table=HannTable(),
	envelope_table=spizazz_envelope,
	frequencies=sol.s2h("re - mi fa - re so - la ti - ^re ^do - so mi - do mi - fa so mi do ", 50 + 12),
	div=3,
	mul=0.35
)
# line = Linseg([(0,0), (5,2000)], loop=True)
# a = Sine(freq=line, mul=[0.3, 0.3]).out()
# line.play()

scope1 = Scope(piano_track)
scope2 = Scope(bass_track)
scope3 = Scope(spizazz_track)
scope7 = Scope(percussion_track)
scope8 = Scope(ladida_track)

sol.s.gui(locals())
