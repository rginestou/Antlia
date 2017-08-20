from .window import Window
from .button import Button
from .label import Label
from .image import Image
from .textinput import TextInput
from .progress import Progress
from .slider import Slider
from .grid import Grid
from .form import Form
from .empty import Empty
from .group import Group

EL_TABLE = {
	"button": Button,
	"grid": Grid,
	"form": Form,
	"label": Label,
	"image": Image,
	"text-input": TextInput,
	"progress": Progress,
	"slider": Slider,
	"group": Group,
	"empty": Empty
}

FORM_TABLE = {
	"text-input": "label"
}
