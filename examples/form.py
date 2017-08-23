# Local testing
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from antlia import *
import time as ti

is_running = True

# Create a GUI based on a layout file and a style file
GUI = Antlia("form_layout", "form_style")

def onFormValidationHandler(form_values):
	is_form_filled = True
	print(form_values)
	for field in form_values:
		if form_values[field] == '':
			# Value missing
			is_form_filled = False
			GUI.change(field, "underline-color", "alizarin")
		elif field.endswith("input"):
			GUI.change(field, "underline-color", "peter-river")

	if is_form_filled:
		print("FILLED")
	else:
		print("Not FILLED")

def minimizeClickHandler():
	GUI.minimizeWindow()

def closeClickHandler():
	global is_running
	is_running = False

# Bind the handler to the button
GUI.bind("main_form", "validation", onFormValidationHandler)
GUI.bind("close_button", "release", closeClickHandler)
GUI.bind("minimize_button", "release", minimizeClickHandler)


# Open the GUI window
GUI.start()

# Main loop, wait for stop event
while not GUI.getUserInfo().want_to_stop and is_running:
	# Give some rest to the CPU
	ti.sleep(0.1)

# Destroy the GUI properly
GUI.quit()
