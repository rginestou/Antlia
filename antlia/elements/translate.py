from .color import Color, lighthen
from ast import literal_eval

def toArrayOfSizes(arg, length=None):
	"""
	Parse an attribute data to get an array of sizes.
	Supported types : px, %, number, ?.
	Raise a custom exception if an error occurs.
	"""
	if arg == "":
		raise Exception("Empty value"); return
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
		# Look for ?
		typ = []
		values = []
		unknown = []
		sum_px = 0
		for i, v in enumerate(array):
			if v.endswith("%"):
				# Percentage
				typ.append("%")
				values.append(float(v[:-1]) / 100.0)
			elif v.endswith("px"):
				# Pixels
				typ.append("px")
				values.append(int(v[:-2]))
				sum_px += int(v[:-2])
			elif v == "?":
				if length is None:
					raise Exception("Can't use '?' in this context"); return
				else:
					unknown.append(i)
					typ.append("px")
					values.append(None)
			else:
				raise Exception("The specified value has no known format"); return

		# Fill ? values
		if length is not None and len(unknown) > 0:
			v = (length - sum_px) / len(unknown)
			for i in unknown:
				values[i] = v
	return values, typ

def toInt(arg):
	res = None
	try:
		res = int(arg)
	except:
		raise Exception("Couldn't convert value to 'int'"); return
	return res

def toFloat(arg):
	res = None
	try:
		res = float(arg)
	except:
		raise Exception("Couldn't convert value to 'float'"); return
	return res

def toBoolean(arg):
	if type(arg) == bool:
		return arg
	if arg == "true":
		return True
	elif arg == "false":
		return False
	else:
		raise Exception("Couldn't convert value to 'bool'")

def toColor(arg):
	try:
		color = Color[arg]
		return color
	except Exception as e:
		pass
	if type(arg) == tuple:
		return arg
	elif arg.startswith("#"):
		hexa = arg[1:]
		if len(hexa) == 6:
			color = []
			for i in range(0, 6, 2):
				color.append(int(hexa[i:i+2], 16))
			color.append(255)
			return color
		else:
			raise Exception("Not a valid color format"); return
	elif arg.startswith("rgb("):
		return tuple(arg[3:]), 255
	elif arg.startswith("rgba("):
		color = literal_eval(arg[4:])
		return color
	else:
		pass
