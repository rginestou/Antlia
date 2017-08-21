On submit, gather all fields from the elements within it.

## Attributes

The `Form` element has the same attributes as the [grid](grid).

## Field elements

These are the only elements and their attributes that will be listed in the fields of a form.

	text-input (label)


## Usage

The `Form` can be filled with any elements. Only some of them, however, can be a field.

Consider the following example of layout:

```json
form main_form
	label hello_label
		.label Fill the form below

	text-input name_input
		.placeholder Enter your name

	button validation_button
		.label Validate
		.form-validation true
```

In this examples, the only field available is the `text-input` content.

In order for a form to be useful, it must contain a button with an attribute `.form-validation` set to `true`. When clicked, the content of all fields will be returned to the corresponding handler.

Using the form within the Python code is easily achieved by defining a handler function and binding it to the `validation` event of the form:

```python
def onFormValidationHandler(form_values):
	pass

GUI.bind("main_form", "validation", onFormValidationHandler)
```
