# python setup.py register -r pypitest
# python setup.py sdist upload -r pypitest

# LIVE

from distutils.core import setup

setup(
	name = 'Antlia',
	packages = ['Antlia'], # this must be the same as the name above
	version = '0.1',
	description = 'Flat Design GUI for Python based on SDL2',
	author = 'Romain Ginestou',
	author_email = 'romain.ginestou@gmail.com',
	url = 'https://github.com/Romaingin/Antlia', # use the URL to the github repo
	download_url = 'https://github.com/Romaingin/Antlia/archive/0.1.tar.gz', # I'll explain this in a second
	keywords = ['SDL2', 'Flat Design', 'GUI'], # arbitrary keywords
	classifiers = [],
)
