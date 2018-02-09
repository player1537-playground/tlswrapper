#!/usr/bin/env python3.6

from distutils.core import setup
from pathlib import Path

setup(
	name='tlswrapper',
	version='1.0',
	description='TLS socket (un)wrapper for plain TCP sockets',
	author='Tanner Hobson',
	author_email='thobson2@vols.utk.edu',
	packages=['tlswrapper'],
	install_requires=[
	],
	entry_points={
		'console_scripts': [
			'tlswrapper=tlswrapper:cli',
		],
	},
)
