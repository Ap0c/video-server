# ----- Imports ----- #

from db import Database


# ----- Functions ----- #

def sync_movies(location):

	"""Dummy function for synchronising movies."""

	pass


def sync_shows(location):

	"""Dummy function for synchronising TV shows."""

	pass


def sync(db_file):

	"""Synchronises the database with the files on disk."""

	if db_file:

		db = Database(db_file)
		media_locations = db.query('SELECT type, path FROM media_locations')

		for location in media_locations:

			if location['type'] == 'movies':
				sync_movies(location['path'])
			elif location['type'] == 'tv_shows':
				sync_shows(location['path'])

	else:
		raise Exception('No db file given.')
