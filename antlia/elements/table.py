from .window import Window
from .button import Button
from .label import Label
from .image import Image
from .textinput import TextInput
from .progress import Progress
from .slider import Slider
from .grid import Grid
from .dropdown import DropDown
from .form import Form
from .checkbox import CheckBox
from .radio import Radio
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
	"check-box": CheckBox,
	"radio": Radio,
	"drop-down": DropDown,
	"group": Group,
	"empty": Empty
}

FORM_TABLE = {
	"text-input": "label",
	"check-box": "state"
}
