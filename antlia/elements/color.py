Color = {
	"turquoise": (26,188,156,255),
	"green-sea": (22,160,133,255),
	"asphalt": (52,73,94,255),
	"wet-asphalt": (44,62,80,255),
	"clouds": (236,240,241,255),
	"silver": (189,195,199,255),
	"concrete": (149,165,166,255),
	"asbestos": (127,140,141,255),
	"peter-river": (52,152,219,255),
	"belize-hole": (41,128,185,255),
	"emerald": (46,204,113,255),
	"nephritis": (39,174,96,255),
	"alizarin": (231,76,60,255),
	"pomegranate": (192,57,43,255),
	"white": (255,255,255,255),
	"dark-grey": (52,52,52,52),
	"grey": (152,152,152,152),
	"light-grey": (212,212,212,212),
	"black": (0,0,0,255),
	"none": None
}

def lighthen(color):
	"""
	Used to slightly lighten a specified color
	"""
	return (min(255, color[0] + 10),
	 		min(255, color[1] + 10),
			min(255, color[2] + 10),
			255)
