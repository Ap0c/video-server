# ----- Imports ----- #

import sqlite3


# ----- Functions ----- #

def query_db(db_file, query, args=()):

	"""Queries the database."""

	db = sqlite3.connect(db_file)
	db.row_factory = sqlite3.Row

	cur = db.execute(query, args)
	results = cur.fetchall()

	db.close()

	return results


def sync_movies(location):

	"""Dummy function for synchronising movies."""

	pass


def sync_shows(location):

	"""Dummy function for synchronising TV shows."""

	pass


def sync(db_file):

	"""Synchronises the database with the files on disk."""

	if db_file:

		media_locations = query_db(db_file,
			'SELECT type, path FROM media_locations')

		for location in media_locations:

			if location['type'] == 'movies':
				sync_movies(location['path'])
			elif location['type'] == 'tv_shows':
				sync_shows(location['path'])

	else:
		raise Exception('No db file given.')
