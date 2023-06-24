from soltracker import *
import wx
import wx.grid as gridlib
import wx.lib.scrolledpanel as scrolled

sol = Soltracker(75)


app = wx.App()
frame = wx.Frame(None, title="SOLTRACKER")
frame.Show()


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


# TITLE:
title_font = wx.Font(60, family = wx.FONTFAMILY_DECORATIVE, style = 1, weight = 90, 
		underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)
title = wx.StaticText(parent=frame, label="soltracker", pos=(20,-10), size=(400, 100))
title.SetFont(title_font.Italic())
title.Show()


# BPM:
bpm_font = wx.Font(20, family = wx.FONTFAMILY_ROMAN, style = 1, weight = 90, 
		underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)
bpm_text = wx.StaticText(parent=frame, label="bpm:", pos=(320, 33), size=(100, 100))
bpm_text.SetFont(bpm_font.Italic())
bpm_text.Show()

bpm_font.SetPointSize(16)
bpm_input = wx.TextCtrl(parent=frame, pos=(320 + 60, 30), size=(70, 30))
bpm_input.SetFont(bpm_font.Italic())
bpm_input.Show()


# TRACKS (!!! variable, depends on client):
track1 = create_ui_track(pos=(0, 90), main_color="#cba6f7")
track2 = create_ui_track(pos=(0, 325 + 90), main_color="#fab387")
tracks = [track1, track2]


def submit_for_playback(self, tracks):
	outputs = []
	for track in tracks:
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

		# Vibrato to control signal:
		vibrato_data = track[6].getPoints()
		new_vibrato_data = []
		for point in vibrato_data:
			new_vibrato_data.append((point[0] * 200*sol.spb/div, math.log10(point[1]*9 + 1)))
		vibrato_param = Linseg(new_vibrato_data).play()
		vibrato_lfo = Sine(freq=vibrato_param*15, mul=vibrato_param/20)

		# Pitch modulation to control signal (including vibrato):
		pitchmod_data = track[5].getPoints()
		new_pitchmod_data = []
		for point in pitchmod_data:
			new_pitchmod_data.append((point[0] * 200*sol.spb/div, point[1]))
		pitchmod_param = Linseg(new_pitchmod_data).play()
		pitchmod_param += vibrato_lfo

		# Generate a track:
		output_track = sol.generate_track(
			wave_table=LinTable(wave_table_data),
			envelope_table=LinTable(envelope_table_data),
			frequencies=sol.s2h(solfege, 49, pitchmod_param),
			div = div,
			mul=[volume_param * (1 - pan_param), volume_param * pan_param]
		).out()

		outputs.append(output_track)

	sol.s.gui(locals())


# SUBMIT BUTTON:
button_font = wx.Font(15, family = wx.FONTFAMILY_ROMAN, style = 1, weight = 90, 
		underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)
button = wx.Button(parent=frame, pos=(460, 30), label="  submit playback  ")
button.SetFont(button_font.Italic())
button.Bind(wx.EVT_BUTTON, lambda event: submit_for_playback(event, tracks))


app.MainLoop()