from antlia import *
import time as ti

# Create a GUI based on a layout file and a style file
GUI = Antlia("layout", "style")

# Define a handler for the button
def buttonClickHandler():
	print("Hello World")

	# Change the content of the label with something else
	GUI.change("hello_label", "text",
			"Hello World !")

# Bind the handler to the button
GUI.bind("hello_button", buttonClickHandler)

# Open the GUI window
GUI.start()

# Main loop, wait for stop event
while not GUI.getUserInfo().want_to_stop:
	ti.sleep(0.1)
	# print("loop")

# Destroy the GUI properly
GUI.quit()
