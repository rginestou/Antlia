# Local testing
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from antlia import *
import time as ti

# Create a GUI based on a layout file and a style file
GUI = Antlia("helloworld_layout")

# Define a handler for the button
def buttonClickHandler():
	# Change the content of the label
	GUI.change("hello_label", "label", "Hello World!")

# Bind the handler to the button
GUI.bind("hello_button", "click", buttonClickHandler)

# Open the GUI window
GUI.start()

# Main loop, wait for stop event
while not GUI.getUserInfo().want_to_stop:
	# Give some rest to the CPU
	ti.sleep(0.1)

# Destroy the GUI properly
GUI.quit()
