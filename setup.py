# python setup.py sdist
# twine upload dist/*

# LIVE

from setuptools import setup, find_packages

setup(
	name = 'antlia',
	packages = find_packages(exclude=['doc', 'examples']), # this must be the same as the name above
	package_data = { 'antlia': ['lib/*', 'resources/*'] },
	version = '0.1.11',
	description = 'Flat Design GUI for Python based on SDL2',
	author = 'Romain Ginestou',
	author_email = 'romain.ginestou@gmail.com',
	url = 'https://github.com/Romaingin/Antlia', # use the URL to the github repo
	download_url = 'https://github.com/Romaingin/Antlia/archive/0.1.tar.gz', # I'll explain this in a second
	keywords = ['SDL2', 'Flat Design', 'GUI'], # arbitrary keywords
	classifiers = [],
	install_requires=['pysdl2', 'colorama']
)
