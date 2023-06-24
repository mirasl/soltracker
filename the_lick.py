from soltracker import *

# s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1, audio="jack").boot()

sol = Soltracker(100)

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
	envelope_table=piano_envelope, 
	frequencies=sol.s2h("do - do - so - so - la - la - so - - - fa - fa - mi - mi - re - re - do - - - so - so - fa - fa - mi - mi - re - - - so - so - fa - fa - mi - mi - re - - - do - do - so - so - la - la - so - - - fa - fa - mi - mi - re - re - do - - - ", 48), 
	div=2,
	mul=0.4
).out()

harmony_track = sol.generate_track(
	wave_table = HarmTable([1, 0, -1/3**2, 0, 1/5**2, 0, -1/7**2, 0, 1/9**2, 0, -1/11**2]),
	envelope_table=spizazz_envelope,
	frequencies=sol.s2h("do mi so mi do mi so mi do fa la fa do mi so mi /ti re fa re do mi so mi /ti re fa re do mi so mi do mi do mi do fa la fa do mi so mi /ti re so re do mi so mi do fa la fa do mi so mi /ti re fa re do mi so mi do mi so mi do fa la fa do mi so mi /ti re fa re do mi so mi /ti re fa re do - ^do - ", 48),
	div=2,
	mul=0.25
).out()
# lfo1 = Sine(freq=.1, mul=500, add=1000)
# lfo2 = Sine(freq=.4).range(2, 8)
# bandpass = ButBP(piano_track[0], freq=lfo1).out()
# bass_track = sol.generate_track(
# 	wave_table=triangle_table, 
# 	envelope_table=CosTable([(0,0),(25,1),(4000,.5),(1892,0)]), 
# 	frequencies=sol.s2h("re so do - ", 50 - 24),
# 	div=0.5, 
# 	mul=0.4
# )
spizazz_track = sol.generate_chord_track(
	wave_table=CosTable(),
	envelope_table=spizazz_envelope,
	frequency_list=[
		sol.s2h("do do do do /ti do /ti do do do do /ti do do do /ti do do do do do do /ti do ", 48 + 12),
		sol.s2h("so so la so so so so so so la so so so la so so so so la so so so so so ", 48),
		sol.s2h("mi mi fa mi fa mi fa mi mi fa mi fa mi fa mi fa mi mi fa mi fa mi fa mi ", 48),
		sol.s2h("do do do do re do re do do do do re do do do re do do do do do do re do ", 48),
	],
	div=0.5,
	mul=[0.15, 0.15]
)

for track in spizazz_track:
	track.out()
# scope_spizazz = Scope(spizazz_track)

percussion_track = sol.generate_noise_track(
	pattern=sol.parse_solfege("do - - - do - do - do - - - do - do - do - - - do - do - do - do do do - do - "),
	div=4,
	envelope_table=LinTable([(0,0), (100,1), (1000,0.2), (8192,0)])
).out()

saw_base_track = sol.generate_track(
	wave_table=HarmTable([1, 1/2, 1/3, 1/4, 1/5, 1/6, 1/7, 1/8, 1/9]),
	envelope_table=LinTable([(0,0), (100,1), (200, 0.8), (8192,0.8)]),
	frequencies=sol.s2h("do mi fa mi re do /so do do fa mi so do fa so so do mi fa mi re do /so do ", 48 - 24),
	div=0.5,
	mul=0.2
).out()


# ladida_track = sol.generate_track(
# 	wave_table=HannTable(),
# 	envelope_table=spizazz_envelope,
# 	frequencies=sol.s2h("re - mi fa - re so - la ti - ^re ^do - so mi - do mi - fa so mi do ", 50 + 12),
# 	div=3,
# 	mul=0.35
# )
# line = Linseg([(0,0), (5,2000)], loop=True)
# a = Sine(freq=line, mul=[0.3, 0.3]).out()
# line.play()

scope1 = Scope(piano_track)
scope2 = Scope(saw_base_track)
scope3 = Scope(spizazz_track)
scope7 = Scope(percussion_track)
scope8 = Scope(harmony_track)

sol.s.gui(locals())
