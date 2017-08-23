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

	typ = []
	values = []
	unknown = []
	sum_px = 0
	multiple = 1
	j = 0
	for i, v in enumerate(array):
		if v.isdigit():
			# Number
			n = int(v)
			if i == len(array) - 1:
				typ += ["%"] * n
				values += [1.0 / n] * n
			else:
				multiple = n
		elif v.endswith("%"):
			# Percentage
			for m in range(multiple):
				typ.append("%")
				values.append(float(v[:-1]) / 100.0)
				j += 1
			multiple = 1
		elif v.endswith("px"):
			# Pixels
			for m in range(multiple):
				typ.append("px")
				values.append(int(v[:-2]))
				sum_px += int(v[:-2])
				j += 1
			multiple = 1
		elif v == "?":
			if length is None:
				raise Exception("Can't use '?' in this context"); return
			else:
				for m in range(multiple):
					unknown.append(j)
					typ.append("px")
					values.append(None)
					j += 1
				multiple = 1
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
