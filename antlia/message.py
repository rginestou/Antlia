from colorama import init

# Support for color in terminal
init()

# Type of errors
ERROR = 0
WARNING = 1
OK = 2

# Colors of errors
class bcolors:
	_FAIL = '\033[91m'
	_OKGREEN = '\033[92m'
	_WARNING = '\033[93m'
	_ENDC = '\033[0m'

# Used to print custom and colored messages
def log(typ, title, content=""):
	"""
	A custom function to draw colorful CLI messages
	"""
	header = ""
	col = bcolors._ENDC
	if typ == ERROR:
		header = "Error: "
		col = bcolors._FAIL
	elif typ == WARNING:
		header = "Warning: "
		col = bcolors._WARNING

	print(col + header + title + bcolors._ENDC)
	print("\t" + content)
