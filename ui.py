import time
import pytermgui as ptg

with ptg.WindowManager() as manager:
	window = (
		ptg.Window(
			"",
			ptg.Label("BPM:", parent_align=ptg.HorizontalAlignment.LEFT),
			ptg.Slider(),
			ptg.InputField("", prompt="Frequencies: "),
			ptg.PixelMatrix(10, 10, default="white"),
			""
		)
	)

	manager.add(window)