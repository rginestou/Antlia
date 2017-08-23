The icon set currently used by Antlia can be found [here](https://material.io/icons/).

## Usage

Adding an icon to the GUI is easy.

Let us take the _explore_ icon from the set for this example.

In the `label` attribute of a label or a button, simply write the name of the icon between `#`:

```json
button icon-button
	.label #explore#
	.text-size 15
```

It will display a 15px large _explore_ icon on the button.
