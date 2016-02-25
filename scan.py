# ----- Imports ----- #

import os

from db import Database


# ----- Functions ----- #

def _read_movies(movie_dir):

	"""Builds a list of movies."""

	movies = []

	for movie in (f for f in os.listdir(movie_dir) if not f.startswith('.')):

		display_name = os.path.splitext(movie)[0].replace('_', ' ').title()
		movie_path = os.path.join(movie_dir, movie)
		movies.append((display_name, movie_path))

	return movies


def _diff_movies(movie_dir, current_movies):

	"""Returns a list of movies to be added, and another of the ids of movies to
	be deleted."""

	to_add = []
	movies = _read_movies(movie_dir)

	for movie in movies:

		already_exists = current_movies.pop(movie[1], None)

		if not already_exists:
			to_add.append(movie)

	to_delete = ((movie,) for movie in current_movies.values())

	return to_add, to_delete


def _sync_movies(db, movie_dir):

	"""Dummy function for synchronising movies."""

	db_movies = db.query('SELECT path, id FROM movies')
	stored_movies = {movie['path']: movie['id'] for movie in db_movies}

	movies_add, movies_delete = _diff_movies(movie_dir, stored_movies)

	db.many('INSERT INTO movies (name, path) VALUES (?, ?)', movies_add)
	db.many('DELETE FROM movies WHERE id = ?', movies_delete)


def _sync_shows(db, location):

	"""Dummy function for synchronising TV shows."""

	pass


def sync(db_file):

	"""Synchronises the database with the files on disk."""

	if db_file:

		db = Database(db_file)
		media_locations = db.query('SELECT type, path FROM media_locations')

		for location in media_locations:

			if location['type'] == 'movies':
				_sync_movies(db, location['path'])
			elif location['type'] == 'tv_shows':
				# _sync_shows(location['path'])
				pass

	else:
		raise Exception('No db file given.')
