from soltracker import *
import wx
import wx.grid as gridlib
import wx.lib.scrolledpanel as scrolled

sol = Soltracker(75)



# class ScrollbarFrame(wx.Frame):
#     def __init__(self):
#         wx.Frame.__init__(self, None, -1, 'Scrollbar Example', size=(300, 200))
#         self.scroll = wx.ScrolledWindow(self, -1)
#         self.scroll.SetScrollbars(1, 1, 600, 400)
#         self.button = wx.Button(self.scroll, -1, "Scroll Me", pos=(50, 20))
#         self.Bind(wx.EVT_BUTTON,  self.OnClickTop, self.button)
#         self.button2 = wx.Button(self.scroll, -1, "Scroll Back", pos=(500, 350))
#         self.Bind(wx.EVT_BUTTON, self.OnClickBottom, self.button2)

#     def OnClickTop(self, event):
#         self.scroll.Scroll(600, 400)
        
#     def OnClickBottom(self, event):
#         self.scroll.Scroll(1, 1)


app = wx.App()
frame = wx.Frame(None, title="SOLTRACKER")
frame.Show()
# scroll = wx.ScrolledWindow(parent=frame)
# scroll.SetScrollbars(1, 1, 600, 400)
# scroll.Show()

# frame = wx.ScrolledWindow(parent=frame1)
# frame.SetScrollRate(10, 10)
# # frame = wx.Panel()
# frame.Show()
# frame.SetScrollbars(1, 1, 10, 10)

# frame = ScrollbarFrame()
# frame.Show()

# panel = wx.Panel()
# scrolled_panel = scrolled.ScrolledPanel(panel)
# scrolled_panel.SetAutoLayout(1)
# scrolled_panel.SetupScrolling()



def create_solfege_table(parent, cell_font : wx.Font, num_cells : int, pos : tuple = (0, 500), cell_size : tuple = (50, 25), color : str = "#f38ba8"):
	solfege_table = []
	for i in range(num_cells):
		widget = wx.TextCtrl(parent=parent, pos=(pos[0] + cell_size[0]*i, pos[1]), size=cell_size)
		widget.BackgroundColour = color
		widget.SetFont(cell_font.Bold())
		widget.SetForegroundColour(wx.WHITE)
		solfege_table.append(widget)
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


# class Track(wx.Panel):
# 	data = []

# 	def __init__(self, parent, cells=200):
# 		wx.Panel.__init__(self, parent)
# 		self.SetBackgroundColour(wx.RED)

# 		solfege_table = create_solfege_table(parent=frame, num_cells=cells, pos=(300, 0))

# 		envelope_table = PyoGuiGrapher(parent=frame, pos=(0, 0), init=[(0.0,0.0), (0.05,1.0), (0.2,0.5), (0.7,0.5), (1.0,0.0)])
# 		envelope_table.Show()

# 		wave_table = PyoGuiGrapher(parent=frame, pos=(0, 200), yrange=(-1, 1), mode=1, init=[(0,0), (0.5,1), (1,0)])
# 		wave_table.Show()

# 		volume_graph = PyoGuiGrapher(parent=frame, pos=(300, 25), size=(50*cells, 75), xlen=cells, yrange=(1, 10), init=[(0,0.5), (1,0.5)])
# 		volume_graph.Show()

# 		pan_graph = PyoGuiGrapher(parent=frame, pos=(300, 100), size=(50*cells, 75), xlen=cells, init=[(0,0.5), (1,0.5)])
# 		pan_graph.Show()

# 		pitchmod_graph = PyoGuiGrapher(parent=frame, pos=(300, 175), size=(50*cells, 75), xlen=cells, yrange=(0, 2), init=[(0,0.5), (1,0.5)])
# 		pitchmod_graph.Show()

# 		vibrato_graph = PyoGuiGrapher(parent=frame, pos=(300, 250), size=(50*cells, 75), xlen=cells, init=[(0,0), (1,0)])
# 		vibrato_graph.Show()

# 		data = [solfege_table, envelope_table, wave_table, volume_graph, pan_graph, pitchmod_graph, vibrato_graph]


def create_ui_track(main_color : str = "#cba6f7", color1 : str = "#acb0be", color2 : str = "#ccd0da", anchor : tuple = (0,0), cells : int = 200, pos : tuple = (0,0)):
	font = wx.Font(14, family = wx.FONTFAMILY_ROMAN, style = 1, weight = 90, underline = False, 
			faceName ="", encoding = wx.FONTENCODING_DEFAULT)
	
	solfege_font = wx.Font(14, family = wx.FONTFAMILY_MAX, style = 1, weight = 90, underline = False, 
			faceName ="", encoding = wx.FONTENCODING_DEFAULT)

	solfege_table = create_solfege_table(parent=frame, cell_font=solfege_font, num_cells=cells, pos=(pos[0] + 300, pos[1] + 0), color="#4c4f69")

	# ENVELOPE:
	envelope_table = PyoGuiGrapher(parent=frame, pos=(pos[0] + 0, pos[1] + 0), size=(300, 162), init=[(0.0,0.0), (0.05,1.0), (0.2,0.5), (0.7,0.5), (1.0,0.0)])
	envelope_table.BackgroundColour = main_color
	envelope_table.Show()

	envelope_text = wx.StaticText(parent=frame, label="envelope", size=(300, 20), pos=(pos[0] + 0, pos[1] + 15), style=wx.ALIGN_CENTER_HORIZONTAL)
	envelope_text.SetFont(font.Italic())
	envelope_text.Show()

	# WAVE:
	wave_table = PyoGuiGrapher(parent=frame, pos=(pos[0] + 0, pos[1] + 162), size=(300, 162), yrange=(-1, 1), mode=1, init=[(0,0), (0.5,1), (1,0)])
	wave_table.BackgroundColour = main_color
	wave_table.Show()

	wave_text = wx.StaticText(parent=frame, label="wave", size=(300, 20), pos=(pos[0] + 0, pos[1] + 15 + 162), style=wx.ALIGN_CENTER_HORIZONTAL)
	wave_text.SetFont(font.Italic())
	wave_text.Show()

	# VOLUME:
	volume_graph = PyoGuiGrapher(parent=frame, pos=(pos[0] + 300, pos[1] + 25), size=(50*cells, 75), xlen=cells, yrange=(1, 10), init=[(0,0.5), (1,0.5)])
	volume_graph.BackgroundColour = color1
	volume_graph.Show()

	volume_text = wx.StaticText(parent=frame, label="volume", pos=(pos[0] + 300 + 35, pos[1] + 25 + 15), style=wx.ALIGN_CENTER_HORIZONTAL)
	volume_text.SetFont(font.Italic())
	volume_text.Show()

	# PAN:
	pan_graph = PyoGuiGrapher(parent=frame, pos=(pos[0] + 300, pos[1] + 100), size=(50*cells, 75), xlen=cells, init=[(0,0.5), (1,0.5)])
	pan_graph.BackgroundColour = color2
	pan_graph.Show()

	pan_text = wx.StaticText(parent=frame, label="pan", pos=(pos[0] + 300 + 35, pos[1] + 100 + 15), size=(50, 20))
	pan_text.SetFont(font.Italic())
	pan_text.Show()

	# PITCHMOD:
	pitchmod_graph = PyoGuiGrapher(parent=frame, pos=(pos[0] + 300, pos[1] + 175), size=(50*cells, 75), xlen=cells, yrange=(0, 2), init=[(0,0.5), (1,0.5)])
	pitchmod_graph.BackgroundColour = color1
	pitchmod_graph.Show()

	pitchmod_text = wx.StaticText(parent=frame, label="pitch modulation", pos=(pos[0] + 300 + 35, pos[1] + 175 + 15), size=(100, 20))
	pitchmod_text.SetFont(font.Italic())
	pitchmod_text.Show()

	# VIBRATO:
	vibrato_graph = PyoGuiGrapher(parent=frame, pos=(pos[0] + 300, pos[1] + 250), size=(50*cells, 75), xlen=cells, init=[(0,0), (1,0)])
	vibrato_graph.BackgroundColour = color2
	vibrato_graph.Show()

	vibrato_text = wx.StaticText(parent=frame, label="vibrato", pos=(pos[0] + 300 + 35, pos[1] + 250 + 15), size=(100, 20))
	vibrato_text.SetFont(font.Italic())
	vibrato_text.Show()

	return [solfege_table, envelope_table, wave_table, volume_graph, pan_graph, pitchmod_graph, vibrato_graph]


title_font = wx.Font(60, family = wx.FONTFAMILY_DECORATIVE, style = 1, weight = 90, 
		underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)
title = wx.StaticText(parent=frame, label="soltracker", pos=(20,-10), size=(400, 100))
title.SetFont(title_font.Italic())
title.Show()

bpm_font = wx.Font(20, family = wx.FONTFAMILY_ROMAN, style = 1, weight = 90, 
		underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)
bpm_text = wx.StaticText(parent=frame, label="bpm:", pos=(320, 33), size=(100, 100))
bpm_text.SetFont(bpm_font.Italic())
bpm_text.Show()

bpm_font.SetPointSize(16)
bpm_input = wx.TextCtrl(parent=frame, pos=(320 + 60, 30), size=(70, 30))
bpm_input.SetFont(bpm_font.Italic())
bpm_input.Show()

# title_font.SetPointSize(15)
# title = wx.StaticText(parent=frame, label="", pos=(310, 5), size=(310, 100))
# title.SetFont(title_font.Italic())
# title.Show()

track1 = create_ui_track(pos=(0, 90), main_color="#cba6f7")
track2 = create_ui_track(pos=(0,325 + 90), main_color="#fab387")


def submit_for_playback(self, track):
	div = 6
	envelope_table_data = multiply_table(track[1].getPoints(), (8191, 1))
	solfege = solfege_table_to_string(track[0])
	wave_table_data = multiply_table(track[2].getPoints(), (8191, 1))

	# Volume graph to control signal:
	volume_data = track[3].getPoints()
	new_volume_data = []
	for point in volume_data:
		new_volume_data.append((point[0] * 200*sol.spb/div, math.log10(9*point[1] + 1)))
	volume_param = Linseg(new_volume_data).play()

	# Pan graph to control signal:
	pan_data = track[4].getPoints()
	new_pan_data = []
	for point in pan_data:
		new_pan_data.append((point[0] * 200*sol.spb/div, point[1]))
	pan_param = Linseg(new_pan_data).play()

	# Vibrato:
	vibrato_data = track[6].getPoints()
	new_vibrato_data = []
	for point in vibrato_data:
		new_vibrato_data.append((point[0] * 200*sol.spb/div, math.log10(point[1]*9 + 1)))
	vibrato_param = Linseg(new_vibrato_data).play()
	vibrato_lfo = Sine(freq=vibrato_param*15, mul=vibrato_param/20)

	# Pitch modulation:
	pitchmod_data = track[5].getPoints()
	new_pitchmod_data = []
	for point in pitchmod_data:
		new_pitchmod_data.append((point[0] * 200*sol.spb/div, point[1]))
	pitchmod_param = Linseg(new_pitchmod_data).play()
	pitchmod_param += vibrato_lfo

	


	# MUSIC CODE:
	# piano_table = HarmTable([1,0.25,0.1875,0.1,0.09,0.09,0.025,0.015])
	# cos_table = CosTable()
	# triangle_table = TriangleTable()

	# piano_envelope = CosTable([(0,0),(50,1),(4000,.5),(8192,0)])
	# spizazz_envelope = LinTable([(0,0),(10,1),(8000,0.4),(8192,0)])
	# cross_stick_envelope = LinTable([(0,1),(10,0.2),(8192,0)])
	# base_envelope = LinTable([(0,0), (400, 1), (4000, 0.5), (8192, 0)])

	# spizazz_volume = Linseg([(0, 0.01), (sol.spb * 16, 0.1)]).play()

	# #spizazz_modulation = Linseg([(0,1), (sol.spb * 16, 2)]).play()
	# spizazz_modulation = Linseg([(0,1)]).play()
	# ladida_vibrato_magnitude = Linseg([(0, 0.00), (sol.spb * 16, 0.06)]).play()
	# ladida_vibrato = LFO(freq=10, mul=ladida_vibrato_magnitude, add=1, type=7)
	# ladida_modulation = Linseg([(0,1)]).play()
	# ladida_modulation += ladida_vibrato

	# eq_freq_shift = Linseg([(0,100), (sol.spb * 16, 5000)]).play()

	# spizazz_track = sol.generate_chord_track(
	# 	wave_table=piano_table,
	# 	envelope_table=spizazz_envelope,
	# 	frequency_list=[
	# 		sol.s2h("so - - so - so fa - fa - fa - mi - - mi - mi mi - mi - mi - " + "so - - so - so fa - fa - fa - mi - - mi - mi mi - mi - mi - " + "so - - so - so fa - fa - fa - mi - - mi - mi mi - mi - mi - " + "so - - so - so fa - fa - fa - mi - - mi - mi mi - mi - mi - " + "so - - so - so fa - fa - fa - mi - - mi - mi mi - mi - mi - " + "so - - so - so fa - fa - fa - mi - - mi - mi mi - mi - mi - " + "so - - so - so fa - fa - fa - me - - me - me re - re - re - "    + "so - - so - so so - so - so - fa - - fa - fa fa - fa - fa - ", 25 + 24, spizazz_modulation),
	# 		sol.s2h("do - - do - do re - re - re - do - - do - do do - do - do - " + "do - - do - do re - re - re - do - - do - do do - do - do - " + "do - - do - do re - re - re - do - - do - do do - do - do - " + "do - - do - do re - re - re - do - - do - do do - do - do - " + "do - - do - do re - re - re - do - - do - do do - do - do - " + "do - - do - do re - re - re - do - - do - do do - do - do - " + "do - - do - do re - re - re - do - - do - do /te - /te - /te - " + "re - - re - re re - re - re - do - - do - do do - do - do - ", 25 + 24, spizazz_modulation),
	# 		sol.s2h("le - - le - le te - te - te - ti - - ti - ti ti - ti - ti - " + "le - - le - le te - te - te - ti - - ti - ti ti - ti - ti - " + "le - - le - le te - te - te - ti - - ti - ti ti - ti - ti - " + "le - - le - le te - te - te - ti - - ti - ti ti - ti - ti - " + "le - - le - le te - te - te - ti - - ti - ti ti - ti - ti - " + "le - - le - le te - te - te - ti - - ti - ti ti - ti - ti - " + "le - - le - le te - te - te - le - - le - le so - so - so - "    + "do - - do - do /ti - /ti - /ti - /te - - /te - /te /la - /la - /la - ", 25 + 12, spizazz_modulation),
	# 		sol.s2h("me - - me - me fa - fa - fa - so - - so - so so - so - so - " + "me - - me - me fa - fa - fa - so - - so - so so - so - so - " + "me - - me - me fa - fa - fa - so - - so - so so - so - so - " + "me - - me - me fa - fa - fa - so - - so - so so - so - so - " + "me - - me - me fa - fa - fa - so - - so - so so - so - so - " + "me - - me - me fa - fa - fa - so - - so - so so - so - so - " + "me - - me - me fa - fa - fa - fa - - fa - fa fa - fa - fa - "    + "- - - - - - - - - - - - - - - - - - - - - - - - ", 25 + 12, spizazz_modulation),
	# 		sol.s2h("fa - - fa - fa so - so - so - do - - do - do do - do - do - " + "fa - - fa - fa so - so - so - do - - do - do do - do - do - " + "fa - - fa - fa so - so - so - do - - do - do do - do - do - " + "fa - - fa - fa so - so - so - do - - do - do do - do - do - " + "fa - - fa - fa so - so - so - do - - do - do do - do - do - " + "fa - - fa - fa so - so - so - do - - do - do do - do - do - " + "fa - - fa - fa so - so - so - le - - le - le te - te - te - "    + "so - - so - so so - so - so - fa - - fa - fa fa - fa - fa - ", 25, spizazz_modulation),
	# 	],
	# 	div = 6,
	# 	mul=[spizazz_volume, spizazz_volume],
	# 	feedback= 1 - (spizazz_volume*10)**0.5
	# )

	# track0 = EQ(spizazz_track[0], eq_freq_shift, 100, -100, 0).out()
	# track1 = EQ(spizazz_track[1], eq_freq_shift, 100, -100, 0).out()
	# track2 = EQ(spizazz_track[2], eq_freq_shift, 100, -100, 0).out()
	# track3 = EQ(spizazz_track[3], eq_freq_shift, 100, -100, 0).out()
	# track4 = EQ(spizazz_track[4], eq_freq_shift, 100, -100, 0).out()

	# cross_stick_track = sol.generate_noise_track(
	# 	pattern=sol.parse_solfege(
	# 		"- - - - - - - - - - - - - - - - - - - - - - - - " +
	# 		"- - - - - - - - - - - - - - - - - - - - - - - - " +
	# 		"do do do di di di re re re ri ri ri mi mi mi fa fa fa fi fi fi so so so " +
	# 		"le le la la te te ti ti ^do ^do ^di ^di ^re ^ri ^mi ^fa ^fi ^so ^si ^la ^li ^ti ^do ^di " +
	# 		"do - do do - do do - do - do - do - do do - do do - do - do - " +
	# 		"do - do do - do do - do - do - do - do do - do do - do - do - " +
	# 		"do - do do - do do - do - do - do - do do - do do - do - do - " +
	# 		"do - do do - do do - do - do - do - do do - do do - do - do - "
	# 	),
	# 	div=6,
	# 	envelope_table=cross_stick_envelope,
	# 	mul=[spizazz_volume, spizazz_volume]
	# ).out()

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
		frequencies=sol.s2h(solfege, 49, pitchmod_param),
		div = div,
		mul=[volume_param * (1 - pan_param), volume_param * pan_param]
	).out()

	sol.s.gui(locals())


button_font = wx.Font(15, family = wx.FONTFAMILY_ROMAN, style = 1, weight = 90, 
		underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)
button = wx.Button(parent=frame, pos=(460, 30), label="  submit playback  ")
button.SetFont(button_font.Italic())
button.Bind(wx.EVT_BUTTON, lambda event: submit_for_playback(event, track1))

app.MainLoop()