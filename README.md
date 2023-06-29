# About

Soltracker is a synthesized music editor based around solfege (do re mi... etc). It is written in python using the pyo library.

Soltracker has two main parts: the "backend," which consists mainly of helper methods which comprehend solfege and waveforms and produces sound using the pyo library, and the gui, a work in progress, meant to allow easier editing of waveforms (it's hard to input every value in a table by typing!)

# Which one do I use?

If you know python and want full control over all features, use the "backend": download just the **soltracker.py** file, import it into a new python script, and use the helper methods provided by the file to create your own songs using the power of typing and solfege! See **no_gui_example.py** for example usage of the soltracker library. The library is simply built on top of the pyo library, so feel free to use any methods from that as well!

The downsides of directly using python are that you cannot view the waveforms as you make them (which makes all control signals like volume, pan, etc a big pain), and you have to know python. The GUI version, which you can launch through **gui.py**, allows you to edit your songs visually by tracing waveforms and typing the solfege.

***The GUI is a work in progress.*** Current incomplete features:
- You cannot scroll, basically rendering the GUI near-useless as you can't make very long songs. Working on this!
- The GUI may be messed up on Windows and Mac computers. It works perfectly on Arch Linux (as of the creation of this file). Future compatibility tests will be necessary!
- Currently, the GUI does not have EQ controls. Still figuring out how to implement this, but as of right now you need to use python and pass it through a pyo EQ filter.
- You cannot save and load songs.

# Installation

1. Install python. The installation can be found at www.python.org and will vary depending on system (follow instructions on the site). Install the most recent stable version of Python 3.

2. Install pip. If on windows, run https://bootstrap.pypa.io/get-pip.py in a browser and take the downloaded file, place it in the same directory as python, and run `python get-pip.py` in the command prompt at the directory.

3. Run the following commands: `pip install pyo` and `pip install wx`.

4. Download the files from this repository and unzip the folder. Run **gui.py** with python to use the gui, or create a new python file starting with `from soltracker import sol` in the same directory and program away!

# Usage

To use the soltracker library with python, you can look at the functions in soltracker.py and see the pyo documentation.

To use the work-in-progress editor: click on any graph to add a point, fill in the boxes with solfege. Leave a box blank if there is no solfege note on that beat. Put a zero in the box to indicate a cutoff for a held note. Add a carat (^) to the beginning of a solfege note (i.e. "^do") to indicate an octave higher. Add a slash (\) to the beginning of a solfege note (i.e. "\do") to indicate an octave lower.

That's all!