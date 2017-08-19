import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from antlia import *
import time as ti
import urllib.request
import threading

# Variables
current_theme = "nature"
is_running = True

# Create a GUI based on a layout file and a style file
GUI = Antlia("gallery_layout", "gallery_style")

def onStart():
	# Add empty images
	for i in range(12):
		GUI.add("image", "img" + str(i), "image_grid", {"padding": "20px"})
	loadTheme(current_theme)

def downloadImage(theme_name, i):
	urllib.request.urlretrieve("https://source.unsplash.com/200x200/?" + theme_name, "gallery_pics/" +theme_name+ str(i) + ".jpg")
	GUI.change("img" + str(i), "source", "gallery_pics\\" + theme_name+str(i) + ".jpg")

def loadTheme(theme_name):
	print("Loading " + theme_name)
	# return
	for i in range(12):
		t = threading.Thread(target=downloadImage, args=(theme_name,i))
		t.start()

# Define a handler for the buttons
def themeClickHandler(theme_name):
	global current_theme
	if theme_name != current_theme:
		loadTheme(theme_name)
		current_theme = theme_name
		GUI.change("theme_info_label", "label", theme_name.upper())

def quitClickHandler():
	global is_running
	is_running = False

# Bind the handlers to the buttons
GUI.bind("leave_button", "click", quitClickHandler)
for theme in ("nature", "sport", "music", "science"):
	GUI.bind("theme_" + theme + ".theme_button",
			"click", themeClickHandler, arg=theme)

GUI.onStart(onStart)

# Open the GUI
GUI.start()

GUI.change("attribute_0", "completed", 60)
# Main loop, wait for stop event
while not GUI.getUserInfo().want_to_stop and is_running:
	# Give some rest to the CPU
	ti.sleep(0.1)

# Destroy the GUI properly
GUI.quit()
