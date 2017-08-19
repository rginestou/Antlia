This examples illustrates a more in-depth use of the *Antlia* library to build a very basic calculator.

The GUI will display an area to show the numbers being added or multiplied, as well as a full numeric pad and some operators buttons.

Here is what will look like our basic calculator:

![Hello World](../images/calculator.png)

## Layout file

We start by creating the layout file. Let's call it `calculator_layout.lia`.

These first two lines specify parameters relevant to the window.

```json
.title Calculator
.resolution 400px 500px
```

The window will thereby have *Calculator* as a title, and a resolution of 400x500px.

The most basic tool to structure a layout is the grid. Like any other element, we declare a grid by writing the `grid` keyword followed by its name, here `main_grid`.

The following two lines are the grid parameters. Here, we only need two rows, the first will take 20% of the space, the other 80%. By default, the `.rows` and `.cols` attributes are set to 1, so there is no need to specify that we only wish one column here.

```json
grid main_grid
	.rows 20% 80%
```

The two rows need to be filled with elements.

Let's add a label to show the result of the calculator's computations.

```json
label result_label
	.label 0
	.text-size 40
	.text-align right
	.padding 0px 15px
	.text-color dark-grey
	.background-color clouds
```

The second row will be filled with another grid. This time, it will have 4 rows and 4 columns. The grid itself will be filled with 16 custom buttons.

```json
grid pad_grid
	.rows 4
	.cols 4

	pad-button 7
	pad-button 8
	pad-button 9
	side-button +
	pad-button 4
	pad-button 5
	pad-button 6
	side-button -
	pad-button 1
	pad-button 2
	pad-button 3
	side-button *
	pad-button clear
		.label C
	pad-button 0
	pad-button enter
		.label =
	side-button /
```

These `pad-button` and `side-button` are not regular elements. They are defined in a _style_ file. Defining custom elements allow us to define attributes such as the color and the text size only once, and then use the custom elements in the layout file, saving a lot of duplicate lines.

## Style file

To declare a new custom element, simply write down its regular type, like `button` in our case, followed by the custom name the layout file will refer to. The newt lines use the same syntax as the layout file.

```json
button pad-button
	.text-size 40

button side-button
	.text-size 40
	.released-color belize-hole
	.pressed-color belize-hole
	.hovered-color belize-hole

```

And that's it.

## Python script

Now, with a new Python script opened, write down the import statements.

```python
from antlia import *
import time as ti
```

Create the GUI based on the layout and style files we just created::

```python
GUI = Antlia("calculator_layout", "calculator_style")
```

For this simple calculator project, we need to store the expression to evaluate. Here, an `expression` list will eventually store two values, and the `operation` string will store the type of operation to apply (add, subtract, multiply or divide).

```python
expression = [0]
operation = None
```

The next thing to do is to define all the handlers to take action when a given button is clicked.

Rather than defining one handler per button, we can define one single `numpadClickHandler` for all the numerical buttons by passing a `digit` parameter to the handler that will contain the digit the button refers to.

The `result` label is changed accordingly.

```python
def numpadClickHandler(digit):
	global expression
	expression[-1] = expression[-1] * 10 + digit

	# Change the content of the label with the new value
	GUI.change("result_label", "label", str(expression[-1]))
```

The `operatorClickHandler` is even simpler.

```python
def operatorClickHandler(operator):
	global operation, expression
	operation = operator
	expression.append(0)
```

The clear button will reset everything.

```python
def clearClickHandler():
	global operation, expression

	expression = [0]
	operation = None

	# Change the content of the label with the new value
	GUI.change("result_label", "label", str(expression[-1]))
```

The last button to take care of is the *enter* button. Since this example is very simple, nothing is done to check if the inputs are correct before evaluating the expression.::

```python
def enterClickHandler():
	global operation, expression
	# Simple example, won't handle errors...
	if operation == "+":
		result = expression[0] + expression[1]
	elif operation == "-":
		result = expression[0] - expression[1]
	elif operation == "*":
		result = expression[0] * expression[1]
	elif operation == "/":
		result = expression[0] / expression[1]

		expression = [result]
		operation = None

		# Change the content of the label with the result
		GUI.change("result_label", "label", str(result))
```

Then comes the bindings. This is just a succession of simple statements. The `arg` value is specified to use a single *handler* function for different buttons.

```python
GUI.bind("0", "click", numpadClickHandler, arg=0)
GUI.bind("1", "click", numpadClickHandler, arg=1)
GUI.bind("2", "click", numpadClickHandler, arg=2)
GUI.bind("3", "click", numpadClickHandler, arg=3)
GUI.bind("4", "click", numpadClickHandler, arg=4)
GUI.bind("5", "click", numpadClickHandler, arg=5)
GUI.bind("6", "click", numpadClickHandler, arg=6)
GUI.bind("7", "click", numpadClickHandler, arg=7)
GUI.bind("8", "click", numpadClickHandler, arg=8)
GUI.bind("9", "click", numpadClickHandler, arg=9)

GUI.bind("+", "click", operatorClickHandler, arg="+")
GUI.bind("-", "click", operatorClickHandler, arg="-")
GUI.bind("*", "click", operatorClickHandler, arg="*")
GUI.bind("/", "click", operatorClickHandler, arg="/")

GUI.bind("clear", "click", clearClickHandler)
GUI.bind("enter", "click", enterClickHandler)
```

Add the remaining lines to make everything work::

```python
# Open the GUI window
GUI.start()

# Main loop, wait for exit event
while not GUI.getUserInfo().want_to_stop:
	# Give some rest to the CPU
	ti.sleep(0.1)

	# Destroy the GUI properly
	GUI.quit()
```

## Full code

Here is the full Python script:

```python
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from antlia import *
import time as ti

# Create a GUI based on a layout file and a style file
GUI = Antlia("examples/calculator_layout", "examples/calculator_style")

# Store the expression to be calculated
expression = [0]
operation = None

# Define handlers for the buttons
def numpadClickHandler(digit):
	global expression
	expression[-1] = expression[-1] * 10 + digit

	# Change the content of the label with the new value
	GUI.change("result_label", "label", str(expression[-1]))

def operatorClickHandler(operator):
	global operation, expression
	operation = operator
	expression.append(0)

def clearClickHandler():
	global operation, expression

	expression = [0]
	operation = None

	# Change the content of the label with the new value
	GUI.change("result_label", "label", str(expression[-1]))

def enterClickHandler():
	global operation, expression
	# Simple example, won't handle errors...
	if operation == "+":
		result = expression[0] + expression[1]
	elif operation == "-":
		result = expression[0] - expression[1]
	elif operation == "*":
		result = expression[0] * expression[1]
	elif operation == "/":
		result = expression[0] / expression[1]

	expression = [result]
	operation = None

	# Change the content of the label with the result
	GUI.change("result_label", "label", str(result))

# Bind the handlers to the buttons
GUI.bind("0", "click", numpadClickHandler, arg=0)
GUI.bind("1", "click", numpadClickHandler, arg=1)
GUI.bind("2", "click", numpadClickHandler, arg=2)
GUI.bind("3", "click", numpadClickHandler, arg=3)
GUI.bind("4", "click", numpadClickHandler, arg=4)
GUI.bind("5", "click", numpadClickHandler, arg=5)
GUI.bind("6", "click", numpadClickHandler, arg=6)
GUI.bind("7", "click", numpadClickHandler, arg=7)
GUI.bind("8", "click", numpadClickHandler, arg=8)
GUI.bind("9", "click", numpadClickHandler, arg=9)

GUI.bind("+", "click", operatorClickHandler, arg="+")
GUI.bind("-", "click", operatorClickHandler, arg="-")
GUI.bind("*", "click", operatorClickHandler, arg="*")
GUI.bind("/", "click", operatorClickHandler, arg="/")

GUI.bind("clear", "click", clearClickHandler)
GUI.bind("enter", "click", enterClickHandler)

# Open the GUI window
GUI.start()

# Main loop, wait for exit event
while not GUI.getUserInfo().want_to_stop:
	# Give some rest to the CPU
	ti.sleep(0.1)

# Destroy the GUI properly
GUI.quit()
```

And the layout file:

```json
.title Calculator
.resolution 400px 500px

grid main_grid
	.rows 20% 80%

	label result_label
		.label 0
		.text-size 40
		.text-align right
		.padding 0px 15px
		.text-color dark-grey
		.background-color clouds

	grid pad_grid
		.rows 4
		.cols 4

		pad-button 7
		pad-button 8
		pad-button 9
		side-button +
		pad-button 4
		pad-button 5
		pad-button 6
		side-button -
		pad-button 1
		pad-button 2
		pad-button 3
		side-button *
		pad-button clear
			.label C
		pad-button 0
		pad-button enter
			.label =
		side-button /
```
