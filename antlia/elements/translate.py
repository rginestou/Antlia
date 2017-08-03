from ..message import log, ERROR, WARNING, OK

def toArrayOfSizes(arg):
	if arg == "":
		log(ERROR, "The specified values are incorrect")
	array = arg.split(" ")
	if array[0][-1] == "%":
		# Percentage
		type_ = "%"
		values = [float(x[:-1]) / 100.0 for x in array]
	elif array[0][-1] == "x":
		# Pixels
		type_ = "px"
		values = [int(x[:-2]) for x in array]
	else:
		print(arg)
	return values, type_

def toInt(arg):
	if type(arg) == int:
		return arg
	return int(arg)

def toBoolean(arg):
	if type(arg) == bool:
		return arg
	if arg == "true":
		return True
	elif arg == "false":
		return False
