from pyo import *

s = Server(duplex=0).boot()

table = SquareTable()
frequency = Linseg([(0, 440), (0.2, 50)]).play()
sound = OscLoop(table=table, freq=frequency, feedback=0, mul=0.2).out()

noise = BrownNoise(mul=frequency / 440).out()

# Starts the recording for 10 seconds...
s.recstart()

s.gui(locals())



# s.gui(locals())

# s.start()

# time.sleep(0.25)

# s.stop()

# from soltracker import *

# sol = Soltracker(10000)

# freq = []
# for i in range(100):
# 	freq.append(130 - i)

# level_up = sol.generate_track(
# 	wave_table=SquareTable(),
# 	envelope_table=sol.envelope_library["spizazz"],
# 	frequencies=freq,
# 	div=1
# ).out()

# sol.s.gui(locals())