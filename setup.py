# ----- Imports ----- #

from setuptools import setup


# ----- Setup ----- #

setup(
	name='Video Server',
	version='0.1',
	packages=['video_server'],
	include_package_data=True,
	zip_safe=False,
	install_requires=['Flask']
)
