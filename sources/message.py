ERROR = 0
WARNING = 1
OK = 2

class bcolors:
	_FAIL = '\033[91m'
	_OKGREEN = '\033[92m'
	_WARNING = '\033[93m'
	_ENDC = '\033[0m'


def log(typ, title, content=""):
	header = ""
	col = bcolors._ENDC
	if typ == ERROR:
		header = "Error: "
		col = bcolors._FAIL
	elif typ == WARNING:
		header = "Warning: "
		col = bcolors._WARNING

	print(col + header + title + bcolors._ENDC)
	print(content)
