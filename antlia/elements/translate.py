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

	if array[0].isdigit():
		# Number
		n = int(arg)
		if len(array) == 1:
			t = "%"
			v = 1.0 / n
		elif len(array) == 2:
			if array[1].endswith("%"):
				# Percentage
				t = "%"
				v = float(array[1][:-1]) / 100.0
			elif array[1].endswith("px"):
				# Pixels
				t = "px"
				v = int(array[1][:-2])
		typ = [t] * n
		values = [v] * n
	else:
		typ = []
		values = []
		for v in array:
			if v.endswith("%"):
				# Percentage
				typ.append("%")
				values.append(float(v[:-1]) / 100.0)
			elif v.endswith("px"):
				# Pixels
				typ.append("px")
				values.append(int(v[:-2]))
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
