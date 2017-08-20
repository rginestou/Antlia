# Local testing
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from antlia import *
import time as ti

# Create a GUI based on a layout file and a style file
GUI = Antlia("form_layout", "form_style")

def onFormValidationHandler(form_values):
	is_form_filled = True
	for field in form_values:
		if form_values[field] == '':
			# Value missing
			is_form_filled = False
			GUI.change(field, "underline-color", "alizarin")
		else:
			GUI.change(field, "underline-color", "peter-river")

	if is_form_filled:
		print("FILLED")
	else:
		print("Not FILLED")

# Bind the handler to the button
GUI.bind("main_form", "validation", onFormValidationHandler)


# Open the GUI window
GUI.start()

# Main loop, wait for stop event
while not GUI.getUserInfo().want_to_stop:
	# Give some rest to the CPU
	ti.sleep(0.1)

# Destroy the GUI properly
GUI.quit()
