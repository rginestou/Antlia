# Antlia
## SDL2-based GUI for Python

_Early development_

_Windows only for the moment_

# Installation

Simply type the following command on a command line:

`pip install antlia`

# Documentation

See the full doc [here](https://antlia.data-ensta.fr/).

# Hello World!

This examples demonstrate how easy it is to come up with a nice-looking GUI with Antlia.

![Hello World](https://antlia.data-ensta.fr/_images/hello_world.png)

`hello_world.py` :

```python
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
```

`helloworld_layout.lia` :

```
.title Hello World
.resolution 600px 200px

grid main_grid
	.rows 100%
	.cols 50% 50%

	button hello_button
		.label Hello
		.text-size 45

	label hello_label
		.label No
		.text-size 45
		.align center
		.text-color dark-grey

```
