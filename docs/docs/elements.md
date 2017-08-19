This page lists all the available elements to compose a GUI, as well as their respective attributes.

## Grid

Used to position other elements within the window.

* **rows** _dimensions_ - number of rows in the grid.

	_Examples_

	`.rows 30% 70%`

	`.rows 20px 10px`

	`.rows 10` (10 equally spaced rows)

	`.rows 4 20px` (4 rows of 20px each)

* **cols** _dimensions_ - number of columns in the grid.

	_See .rows for examples_

* **padding** _dimensions_ - padding to apply to the grid.

	_See padding for examples_

* **background-color** _color_ - color of the grid's background.

	_Examples_

	`.background-color clouds`

	`.background-color rgb(55, 120, 102)`

* **drag-window** _boolean_ - dragging this grid will result in the whole window moving


## Button

Can be clicked to trigger actions.

* **label** _string_ - The text to be displayed on the button.

	_Examples_

	`.label This is a button`

	`.label #icon-name#`

* **state** _released/hovered/pressed_ - state of the button.


* **font** _string/path_ - label's font.

	_Examples_

	`.font lato-light`

* **text-size** _integer_ - size of the text in pixels.

* **text-color** _color_ - color of the text.

* **text-align** _left/center/right_ - position of the text in the button.

	_Examples_

	`.text-align center`


* **released-color** _color_ - color of the button when released.

* **hovered-color** _color_ - color of the button when released.

* **pressed-color** _color_ - color of the button when released.

* **drag-window** _boolean_ - dragging this grid will result in the whole window moving
