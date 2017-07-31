Color = {
	"turquoise": (26,188,156,255),
	"green_sea": (22,160,133,255),
	"asphalt": (52,73,94,255),
	"wet_asphalt": (44,62,80,255),
	"clouds": (236,240,241,255),
	"silver": (189,195,199,255),
	"concrete": (149,165,166,255),
	"asbestos": (127,140,141,255),
	"peter_river": (52,152,219,255),
	"belize_hole": (41,128,185,255),
	"white": (255,255,255,255),
	"dark_grey": (52,52,52,52),
	"black": (0,0,0,255)
}

def lighthen(color):
	"""
	Used to slightly lighten a specified color
	"""
	return (min(255, color[0] + 7),
	 		min(255, color[1] + 7),
			min(255, color[2] + 7),
			255)
