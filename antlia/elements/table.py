from .window import Window
from .button import Button
from .label import Label
from .image import Image
from .progress import Progress
from .grid import Grid
from .empty import Empty

EL_TABLE = {
	"button": Button,
	"grid": Grid,
	"label": Label,
	"image": Image,
	"progress": Progress,
	"empty": Empty
}
