from soltracker import *

# s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1, audio="jack").boot()

piano_table = tone_library["piano"]
cos_table = CosTable()
triangle_table = TriangleTable()

piano_envelope = envelope_library["piano"]
spizazz_envelope = envelope_library["spizazz"]

piano_track = generate_track(
	wave_table=tone_library["piano"], 
	envelope_table=spizazz_envelope, 
	frequencies=s2h("la - ti ^do - ^re la ti - so - la - - - - - - - - - - - - ", 50), 
	base_duration=0.07 * 4/3,
	mul=0.25
)
bass_track = generate_track(
	wave_table=triangle_table, 
	envelope_table=CosTable([(0,0),(25,1),(4000,.5),(1892,0)]), 
	frequencies=s2h("re so do - ", 50 - 24),
	base_duration=0.56, 
	mul=0.4
)
spizazz_track = generate_chord_track(
	wave_table=CosTable(),
	envelope_table=spizazz_envelope,
	frequency_list=[
			s2h("fa fa mi - ", 50),
			s2h("^do ti ti - ", 50),
			s2h("^mi ^mi ^re - ", 50),
			s2h("^la ^le ^so - ", 50),
				],
	base_duration=0.56
)
percussion_track = generate_noise_track(
	pattern=parse_solfege("fi - - fi - fi fi - - fi - fi fi - - fi - fi fi - fi ^fi ^do do "),
	base_duration=0.28/3,
	envelope_table=spizazz_envelope
)
ladida_track = generate_track(
	wave_table=HannTable(),
	envelope_table=spizazz_envelope,
	frequencies=s2h("re - mi fa - re so - la ti - ^re ^do - so mi - do mi - fa so mi do ", 50 + 12),
	base_duration=0.28/3,
	mul=0.35
)

scope1 = Scope(piano_track)
scope2 = Scope(bass_track)
scope3 = Scope(spizazz_track)
scope4 = Scope(percussion_track)
scope5 = Scope(ladida_track)

s.gui(locals())
