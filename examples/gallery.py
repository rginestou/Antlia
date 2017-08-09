import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from antlia import *
import time as ti
import urllib.request

# Create a GUI based on a layout file and a style file
GUI = Antlia("examples/gallery_layout", "examples/gallery_style")

# Bind the handlers to the buttons
# GUI.bind("open-file_button", "click", openClickHandler)
# GUI.bind("quit_button", "click", quitClickHandler)
#
# GUI.bind("play-pause_button", "click", playPauseClickHandler)
# GUI.bind("stop_button", "click", stopClickHandler)

# Open the GUI
GUI.start()

# urllib.request.urlretrieve("https://source.unsplash.com/200x200/?nature,water", "examples/gallery_pics/water_1.jpg")

# Main loop, wait for stop event
while not GUI.getUserInfo().want_to_stop:

	# Give some rest to the CPU
	ti.sleep(0.1)

# Destroy the GUI properly
GUI.quit()
