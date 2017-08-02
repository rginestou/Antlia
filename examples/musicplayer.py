import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from antlia import *
import time as ti
from tinytag import TinyTag
#
# tag = TinyTag.get('/some/music.mp3', image=True)
# image_data = tag.get_image()

# Create a GUI based on a layout file and a style file
GUI = Antlia("examples/musicplayer_layout")

# Define a handler for the button
def quitClickHandler():
	GUI.stop()

def openClickHandler():
	# Change the content of the label with something else
	file_path = GUI.openFileDialog("Open a song", ".mp3", "", None)

	if file_path is not None:
		pass

	# from pygame import mixer # Load the required library

	# mixer.init()
	# mixer.music.load('D:/ghost.mp3')
	# mixer.music.play()
	# ti.sleep(1)
	# mixer.music.stop()

# Bind the handler to the button
GUI.bind("open-file_button", "click", openClickHandler)
GUI.bind("quit_button", "click", quitClickHandler)


# Open the GUI window
GUI.start()

# Main loop, wait for stop event
while not GUI.getUserInfo().want_to_stop:
	# Give some rest to the CPU
	ti.sleep(0.1)

# Destroy the GUI properly
GUI.quit()
