# from soltracker import *

# #s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1, audio="jack").boot()

# piano_table = HarmTable([1,0.25,0.1875,0.1,0.09,0.09,0.025,0.015])
# cos_table = CosTable()
# triangle_table = TriangleTable()

# piano_envelope = CosTable([(0,0),(50,1),(4000,.5),(8192,0)])
# spizazz_envelope = LinTable([(0,0),(10,1),(8000,0.1),(8192,0)])

# spizazz_volume = Linseg([(0, 0.01), (24*0.15*4, 0.1)]).play()

# # piano_track = generate_track(
# # 	wave_table=piano_table,
# # 	envelope_table=piano_envelope,
# # 	frequencies=s2h("do do so so la la so - fa fa mi mi re re do - so so fa fa mi mi re - so so fa fa mi mi re - ", 50),
# # 	base_duration=0.5,
# # 	mul=[0.1,0.1]
# # )

# spizazz_track = generate_chord_track(
# 	wave_table=cos_table,
# 	envelope_table=spizazz_envelope,
# 	frequency_list=[
# 		s2h("so - - so - so fa - fa - fa - mi - - mi - mi mi - mi - mi - ", 25 + 24),
# 		s2h("do - - do - do re - re - re - do - - do - do do - do - do - ", 25 + 24),
# 		s2h("le - - le - le te - te - te - ti - - ti - ti ti - ti - ti - ", 25 + 12),
# 		s2h("me - - me - me fa - fa - fa - so - - so - so so - so - so - ", 25 + 12),
# 		s2h("fa - - fa - fa so - so - so - do - - do - do do - do - do - ", 25),
# 	],
# 	div = 0.15,
# 	mul=[spizazz_volume, spizazz_volume]
# )

# scope = Scope(spizazz_track)

# s.gui(locals())