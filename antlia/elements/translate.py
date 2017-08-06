from ..message import log, ERROR, WARNING, OK

def toArrayOfSizes(arg):
	"""
	Parse an attribute data to get an array of sizes.
	Supported types : px, %, number.
	"""
	if arg == "":
		err = "The specified value is incorrect"
		return None, None, err
	array = arg.split(" ")
	if array[0].endswith("%"):
		# Percentage
		typ = "%"
		values = [float(x[:-1]) / 100.0 for x in array]
	elif array[0].endswith("x"):
		# Pixels
		typ = "px"
		values = [int(x[:-2]) for x in array]
	elif arg.isdigit():
		# Number
		n = int(arg)
		typ = "%"
		values = [1.0 / n for _ in range(n)]
	else:
		err = "The specified value has no known format"
		return None, None, err
	return values, typ, None

def toInt(arg):
	if type(arg) == int:
		return arg
	return int(arg)

def toFloat(arg):
	if type(arg) == float:
		return arg
	return float(arg)

def toBoolean(arg):
	if type(arg) == bool:
		return arg
	if arg == "true":
		return True
	elif arg == "false":
		return False
