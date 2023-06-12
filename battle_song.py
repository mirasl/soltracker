from soltracker import *
# import matplotlib.pyplot as plt
# import numpy as np
# import pylustrator

# pylustrator.start()

# plt.style.use('_mpl-gallery')

# # make the data
# np.random.seed(3)
# x = 4 + np.random.normal(0, 2, 24)
# y = 4 + np.random.normal(0, 2, len(x))
# # size and color:
# sizes = np.random.uniform(15, 80, len(x))
# colors = np.random.uniform(15, 80, len(x))

# # plot
# fig, ax = plt.subplots()

# ax.scatter(x, y, s=sizes, c=colors, vmin=0, vmax=100)

# ax.set(xlim=(0, 8), xticks=np.arange(1,8),
# 		ylim=(0, 8), yticks=np.arange(1,8))
	
# plt.ion = True
# plt.show()

#s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1, audio="jack").boot()

sol = Soltracker(75)

piano_table = HarmTable([1,0.25,0.1875,0.1,0.09,0.09,0.025,0.015])
cos_table = CosTable()
triangle_table = TriangleTable()

piano_envelope = CosTable([(0,0),(50,1),(4000,.5),(8192,0)])
spizazz_envelope = LinTable([(0,0),(10,1),(8000,0.4),(8192,0)])
cross_stick_envelope = LinTable([(0,1),(10,0.2),(8192,0)])
base_envelope = LinTable([(0,0), (400, 1), (4000, 0.5), (8192, 0)])

spizazz_volume = Linseg([(0, 0.01), (sol.spb * 16, 0.1)]).play()

#spizazz_modulation = Linseg([(0,1), (sol.spb * 16, 2)]).play()
spizazz_modulation = Linseg([(0,1)]).play()
ladida_vibrato_magnitude = Linseg([(0, 0.00), (sol.spb * 16, 0.06)]).play()
ladida_vibrato = LFO(freq=10, mul=ladida_vibrato_magnitude, add=1, type=7)
ladida_modulation = Linseg([(0,1)]).play()
ladida_modulation += ladida_vibrato

eq_freq_shift = Linseg([(0,100), (sol.spb * 16, 5000)]).play()

# piano_track = generate_track(
# 	wave_table=piano_table,
# 	envelope_table=piano_envelope,
# 	frequencies=s2h("do do so so la la so - fa fa mi mi re re do - so so fa fa mi mi re - so so fa fa mi mi re - ", 50),
# 	base_duration=0.5,
# 	mul=[0.1,0.1]
# )

spizazz_track = sol.generate_chord_track(
	wave_table=piano_table,
	envelope_table=spizazz_envelope,
	frequency_list=[
		sol.s2h("so - - so - so fa - fa - fa - mi - - mi - mi mi - mi - mi - " + "so - - so - so fa - fa - fa - mi - - mi - mi mi - mi - mi - " + "so - - so - so fa - fa - fa - mi - - mi - mi mi - mi - mi - " + "so - - so - so fa - fa - fa - mi - - mi - mi mi - mi - mi - " + "so - - so - so fa - fa - fa - mi - - mi - mi mi - mi - mi - " + "so - - so - so fa - fa - fa - mi - - mi - mi mi - mi - mi - " + "so - - so - so fa - fa - fa - me - - me - me re - re - re - "    + "so - - so - so so - so - so - fa - - fa - fa fa - fa - fa - ", 25 + 24, spizazz_modulation),
		sol.s2h("do - - do - do re - re - re - do - - do - do do - do - do - " + "do - - do - do re - re - re - do - - do - do do - do - do - " + "do - - do - do re - re - re - do - - do - do do - do - do - " + "do - - do - do re - re - re - do - - do - do do - do - do - " + "do - - do - do re - re - re - do - - do - do do - do - do - " + "do - - do - do re - re - re - do - - do - do do - do - do - " + "do - - do - do re - re - re - do - - do - do /te - /te - /te - " + "re - - re - re re - re - re - do - - do - do do - do - do - ", 25 + 24, spizazz_modulation),
		sol.s2h("le - - le - le te - te - te - ti - - ti - ti ti - ti - ti - " + "le - - le - le te - te - te - ti - - ti - ti ti - ti - ti - " + "le - - le - le te - te - te - ti - - ti - ti ti - ti - ti - " + "le - - le - le te - te - te - ti - - ti - ti ti - ti - ti - " + "le - - le - le te - te - te - ti - - ti - ti ti - ti - ti - " + "le - - le - le te - te - te - ti - - ti - ti ti - ti - ti - " + "le - - le - le te - te - te - le - - le - le so - so - so - "    + "do - - do - do /ti - /ti - /ti - /te - - /te - /te /la - /la - /la - ", 25 + 12, spizazz_modulation),
		sol.s2h("me - - me - me fa - fa - fa - so - - so - so so - so - so - " + "me - - me - me fa - fa - fa - so - - so - so so - so - so - " + "me - - me - me fa - fa - fa - so - - so - so so - so - so - " + "me - - me - me fa - fa - fa - so - - so - so so - so - so - " + "me - - me - me fa - fa - fa - so - - so - so so - so - so - " + "me - - me - me fa - fa - fa - so - - so - so so - so - so - " + "me - - me - me fa - fa - fa - fa - - fa - fa fa - fa - fa - "    + "- - - - - - - - - - - - - - - - - - - - - - - - ", 25 + 12, spizazz_modulation),
		sol.s2h("fa - - fa - fa so - so - so - do - - do - do do - do - do - " + "fa - - fa - fa so - so - so - do - - do - do do - do - do - " + "fa - - fa - fa so - so - so - do - - do - do do - do - do - " + "fa - - fa - fa so - so - so - do - - do - do do - do - do - " + "fa - - fa - fa so - so - so - do - - do - do do - do - do - " + "fa - - fa - fa so - so - so - do - - do - do do - do - do - " + "fa - - fa - fa so - so - so - le - - le - le te - te - te - "    + "so - - so - so so - so - so - fa - - fa - fa fa - fa - fa - ", 25, spizazz_modulation),
	],
	div = 6,
	mul=[spizazz_volume, spizazz_volume],
	feedback= 1 - (spizazz_volume*10)**0.5
)

# melody_track = sol.generate_track(
# 	wave_table=cos_table,
# 	envelope_table=spizazz_envelope,
# 	frequencies=sol.s2h(
# 		"- - - - - - - - - - - - - - - - - - - - - - - - " +
# 		"- - - - - - - - - - - - - - - - - - - - - - - - " +
# 		"- - - - - - - - - - - - - - - - - - - - - - - - " +
# 		"- - - - - - - - - - - - - - - - - - - - do re me fa " +
# 		"so - - do - so fa me re - fa - mi - - - - - do - - re me fa " +
# 		"so - - do - so fa - te - fa - so - - - - - - - do re me fa " +
# 		"so - - do - so fa me re - fa - me - - /le - me re do /te - re - " +
# 		"do - - - - - - /ti - - - - - /te - - - - - /la - - - - - "
# 		, 49),
# 	div = 6,
# 	mul=[0.5,0.5]
# ).out()

solfege = ("0 - - - - - - - - - - - - - - - - - - - - - - - " +
	"- - - - - - - - - - - - - - - - - - - - - - - - " +
	"- - - - - - - - - - - - - - - - - - - - - - - - " +
	"- - - - - - - - - - - - - - - - - - - - do re me fa " +
	"so - - do - so fa me re - fa - mi - - - 0 - do - - re me fa " +
	"so - - do - so fa - te - fa - so - - - - - 0 - do re me fa " +
	"so - - do - so fa me re - fa - me - - /le - me re do /te - re - " +
	"do - - - - - /ti - - - - - /te - - - - - /la - - - - - ")

melody_track = sol.generate_track(
	wave_table=HarmTable([1, 0, 1/3, 0, 1/5, 0, 1/7, 0, 1/9, 0, 1/11, 0, 1/13, 0, 1/15, 0, 1/17, 0, 1/19]),
	envelope_table=LinTable([(0,1), (8192,1)]),
	frequencies=sol.s2h(solfege, 49),
	div = 6,
	mul=[0.1,0.1]
).out()


# for track in spizazz_track:
# 	track.out()
track0 = EQ(spizazz_track[0], eq_freq_shift, 100, -100, 0).out()
track1 = EQ(spizazz_track[1], eq_freq_shift, 100, -100, 0).out()
track2 = EQ(spizazz_track[2], eq_freq_shift, 100, -100, 0).out()
track3 = EQ(spizazz_track[3], eq_freq_shift, 100, -100, 0).out()
track4 = EQ(spizazz_track[4], eq_freq_shift, 100, -100, 0).out()
	#track.out()

cross_stick_track = sol.generate_noise_track(
	pattern=sol.parse_solfege(
		"- - - - - - - - - - - - - - - - - - - - - - - - " +
		"- - - - - - - - - - - - - - - - - - - - - - - - " +
		"do do do di di di re re re ri ri ri mi mi mi fa fa fa fi fi fi so so so " +
		"le le la la te te ti ti ^do ^do ^di ^di ^re ^ri ^mi ^fa ^fi ^so ^si ^la ^li ^ti ^do ^di " +
		"do - do do - do do - do - do - do - do do - do do - do - do - " +
		"do - do do - do do - do - do - do - do do - do do - do - do - " +
		"do - do do - do do - do - do - do - do do - do do - do - do - " +
		"do - do do - do do - do - do - do - do do - do do - do - do - "
	),
	div=6,
	envelope_table=cross_stick_envelope,
	mul=[spizazz_volume, spizazz_volume]
).out()

# ladida = sol.generate_track(
# 	wave_table=SquareTable(),
# 	envelope_table=LinTable([(0,1),(8191,1)]),
# 	frequencies=sol.s2h("so - - do - so fa me re - fa - mi - - - - - do - - re me fa ", 25 + 24, ladida_modulation),
# 	div=6,
# 	mul=[spizazz_volume, spizazz_volume]
# )

# scope = Scope(spizazz_track)
scope1 = Scope(melody_track)
scope2 = Scope(spizazz_track)
scope3 = Scope(cross_stick_track)

sol.s.gui(locals())