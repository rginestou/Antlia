import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from antlia import *
import time as ti

# Create a GUI based on a layout file and a style file
GUI = Antlia("examples/calculator_layout")

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
