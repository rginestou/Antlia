Elements
=================
This section describes all the elements that can be used to make a GUI using *Antlia*.

Grid
-----------------
.. py:attribute:: grid

	The *Grid* is used to build the structure of the GUI.

	:param rows: The number of the rows or their proportions
	:param cols: The number of the columns or their proportions

	:param background-color: The color of the background (apply to all te *Grid*)

Button
-----------------
.. py:attribute:: button

	The *Button* has different states and will fire events when the user interacts with it.

	:param str label: What is written on the button
	:param released,pressed,hovered,disabled state: The state of the button, will affect the way it is displayed
	:param center,left,right text-align: The alignment of the label

	:param color released-color: The color of the button once it is released
	:param color pressed-color: The color of the button once it is pressed
	:param color hovered-color: The color of the button once it is hovered
	:param color text-color: The color of label
