from soltracker import *

s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1, audio="jack").boot()

piano_table = HarmTable([1,0.25,0.1875,0.1,0.09,0.09,0.025,0.015])
cos_table = CosTable()
triangle_table = TriangleTable()

piano_envelope = CosTable([(0,0),(50,1),(4000,.5),(8192,0)])
spizazz_envelope = LinTable([(0,0),(10,1),(8000,0.1),(8192,0)])

