from soltracker import *

#s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1, audio="jack").boot()

sol = Soltracker(75)

piano_table = HarmTable([1,0.25,0.1875,0.1,0.09,0.09,0.025,0.015])
cos_table = CosTable()
triangle_table = TriangleTable()

piano_envelope = CosTable([(0,0),(50,1),(4000,.5),(8192,0)])
spizazz_envelope = LinTable([(0,0),(10,1),(8000,0.1),(8192,0)])
cross_stick_envelope = LinTable([(0,1),(10,0.2),(8192,0)])

spizazz_volume = Linseg([(0, 0.01), (sol.spb * 16, 0.1)]).play()

spizazz_modulation = Linseg([(0,1), (sol.spb * 16, 2)]).play()

# piano_track = generate_track(
# 	wave_table=piano_table,
# 	envelope_table=piano_envelope,
# 	frequencies=s2h("do do so so la la so - fa fa mi mi re re do - so so fa fa mi mi re - so so fa fa mi mi re - ", 50),
# 	base_duration=0.5,
# 	mul=[0.1,0.1]
# )

spizazz_track = sol.generate_chord_track(
	wave_table=cos_table,
	envelope_table=spizazz_envelope,
	frequency_list=[
		sol.s2h("so - - so - so fa - fa - fa - mi - - mi - mi mi - mi - mi - ", 25 + 24, spizazz_modulation),
		sol.s2h("do - - do - do re - re - re - do - - do - do do - do - do - ", 25 + 24, spizazz_modulation),
		sol.s2h("le - - le - le te - te - te - ti - - ti - ti ti - ti - ti - ", 25 + 12, spizazz_modulation),
		sol.s2h("me - - me - me fa - fa - fa - so - - so - so so - so - so - ", 25 + 12, spizazz_modulation),
		sol.s2h("fa - - fa - fa so - so - so - do - - do - do do - do - do - ", 25, spizazz_modulation),
	],
	div = 6,
	mul=[spizazz_volume, spizazz_volume],
	feedback= 1 - spizazz_volume*10
)

# cross_stick_track = sol.generate_noise_track(
# 	pattern=sol.parse_solfege(
# 			"- - - - - - - - - - - - - - - - - - - - - - - - " +
# 			"- - - - - - - - - - - - - - - - - - - - - - - - " +
# 			"do do do di di di re re re ri ri ri mi mi mi fa fa fa fi fi fi so so so " +
# 			"le le la la te te ti ti ^do ^do ^di ^di ^re ^ri ^mi ^fa ^fi ^so ^si ^la ^li ^ti ^do ^di "
# 	),
# 	div=6,
# 	envelope_table=cross_stick_envelope,
# 	mul=[spizazz_volume, spizazz_volume]
# )

# ladida = sol.generate_track(
# 	wave_table=HannTable(),
# 	envelope_table=spizazz_envelope,
# 	frequencies=sol.s2h("- - - - - - - - - - - - - - - - - - - - - - - - " +
# 			"- - - - - - - - - - - - - - - - - - - - - - - - " +
# 			"do do do di di di re re re ri ri ri mi mi mi fa fa fa fi fi fi so so so " +
# 			"le le la la te te ti ti ^do ^do ^di ^di ^re ^ri ^mi ^fa ^fi ^so ^si ^la ^li ^ti ^do ^di ", 50),
# 	div=6,
# 	mul=[spizazz_volume, spizazz_volume]
# )

scope = Scope(spizazz_track)

sol.s.gui(locals())