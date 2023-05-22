from main import *

s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1, audio="jack").boot()

piano_table = HarmTable([1,0.25,0.1875,0.1,0.09,0.09,0.025,0.015])
cos_table = CosTable()
triangle_table = TriangleTable()

piano_envelope = CosTable([(0,0),(50,1),(4000,.5),(8192,0)])
spizazz_envelope = LinTable([(0,0),(10,1),(8000,0.1),(8192,0)])

piano_track = generate_track(
	wave_table=piano_table, 
	envelope_table=piano_envelope, 
	frequencies=s2h("re - mi fa - so re mi - do - re - - - - - - - - - - - - ", 57), 
	base_duration=0.07 * 4/3,
	mul=0.25
)
triangle_track = generate_track(
	wave_table=triangle_table, 
	envelope_table=CosTable([(0,0),(25,1),(4000,.5),(1892,0)]), 
	frequencies=s2h("re so do - ", 50 - 24),
	base_duration=0.56, 
	mul=0.4
)
spizazz_track1 = generate_track(
	wave_table=CosTable(),
	envelope_table=spizazz_envelope,
	frequencies=s2h("fa fa mi - ", 50),
	base_duration=0.56
)
spizazz_track2 = generate_track(
	wave_table=CosTable(),
	envelope_table=spizazz_envelope,
	frequencies=s2h("do ti ti - ", 50),
	base_duration=0.56
)
spizazz_track3 = generate_track(
	wave_table=CosTable(),
	envelope_table=spizazz_envelope,
	frequencies=s2h("mi me re - ", 50),
	base_duration=0.56
)
spizazz_track4 = generate_track(
	wave_table=CosTable(),
	envelope_table=spizazz_envelope,
	frequencies=s2h("la le so - ", 50),
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
scope2 = Scope(triangle_track)
scope3 = Scope(spizazz_track1)
scope4 = Scope(spizazz_track2)
scope5 = Scope(spizazz_track3)
scope6 = Scope(spizazz_track4)
scope7 = Scope(percussion_track)

s.gui(locals())
