from soltracker import *
import wx
import wx.grid as gridlib

sol = Soltracker(75)

app = wx.App()
frame = wx.Frame(None, title="Hello World")
frame.Show()

slider = PyoGuiControlSlider(parent=frame, minvalue=0, maxvalue=1)
slider.Show()


def create_solfege_table(parent, num_cells : int, pos : tuple = (0, 500), cell_size : tuple = (50, 25)):
	solfege_table = []
	for i in range(num_cells):
		solfege_table.append(wx.TextCtrl(parent=parent, pos=(pos[0], pos[1] + cell_size[1]*i), 
				size=cell_size))
		solfege_table[i].Show()
	return solfege_table


def solfege_table_to_string(solfege_table : list):
	solfege = ""
	for cell in solfege_table:
		cell_value = cell.GetValue()
		if cell_value == "":
			solfege += "- "
		else:
			solfege += cell_value + " "
	return solfege


def multiply_table(table : list, coefficient : tuple):
	new_table = []
	for point in table:
		new_table.append((int(point[0] * coefficient[0]), point[1] * coefficient[1]))
	return new_table

def create_ui_track():
	solfege_table = create_solfege_table(parent=frame, num_cells=200, pos=(0, 200))

	envelope_table = PyoGuiGrapher(parent=frame)
	envelope_table.Show()

	wave_table = PyoGuiGrapher(parent=frame, pos=(300, 0), yrange=(-1, 1), mode=1)
	wave_table.Show()

	

	return [solfege_table, envelope_table, wave_table]

track1 = create_ui_track()


def submit_for_playback(self, track):
	envelope_table_data = multiply_table(track[1].getPoints(), (8191, 1))
	solfege = solfege_table_to_string(track[0])
	wave_table_data = multiply_table(track[2].getPoints(), (8191, 1))
	print(solfege)

	# MUSIC CODE:
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

	track0 = EQ(spizazz_track[0], eq_freq_shift, 100, -100, 0).out()
	track1 = EQ(spizazz_track[1], eq_freq_shift, 100, -100, 0).out()
	track2 = EQ(spizazz_track[2], eq_freq_shift, 100, -100, 0).out()
	track3 = EQ(spizazz_track[3], eq_freq_shift, 100, -100, 0).out()
	track4 = EQ(spizazz_track[4], eq_freq_shift, 100, -100, 0).out()

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

	# solfege = ("0 - - - - - - - - - - - - - - - - - - - - - - - " +
	# 	"- - - - - - - - - - - - - - - - - - - - - - - - " +
	# 	"- - - - - - - - - - - - - - - - - - - - - - - - " +
	# 	"- - - - - - - - - - - - - - - - - - - - do re me fa " +
	# 	"so - - do - so fa me re - fa - mi - - - 0 - do - - re me fa " +
	# 	"so - - do - so fa - te - fa - so - - - - - 0 - do re me fa " +
	# 	"so - - do - so fa me re - fa - me - - /le - me re do /te - re - " +
	# 	"do - - - - - /ti - - - - - /te - - - - - /la - - - - - ")

	melody_track = sol.generate_track(
		wave_table=LinTable(wave_table_data),
		envelope_table=LinTable(envelope_table_data),
		frequencies=sol.s2h(solfege, 49),
		div = 6,
		mul=[0.1,0.1]
	).out()

	sol.s.gui(locals())


button = wx.Button(parent=frame)
button.Bind(wx.EVT_BUTTON, lambda event: submit_for_playback(event, track1))

app.MainLoop()