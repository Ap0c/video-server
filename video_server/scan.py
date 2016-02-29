# ----- Imports ----- #

import os
import re

from .db import Database


# ----- Functions ----- #

def _is_dir(path, directory):

	"""Checks if something is a directory."""

	fullpath = os.path.join(path, directory)
	return os.path.isdir(fullpath)


def _read_movies(movie_dir):

	"""Builds a list of movies."""

	movie_path = movie_dir['path']
	movies = []

	for movie in (f for f in os.listdir(movie_path) if not f.startswith('.')):

		display_name = os.path.splitext(movie)[0].replace('_', ' ').title()
		movie_path = os.path.join(str(movie_dir['id']), movie)
		movies.append((display_name, movie_path))

	return movies


def _get_seasons(tv_dir, show):

	"""Retrieves the show's episodes as a dictionary of seasons."""

	show_path = os.path.join(tv_dir['path'], show)
	seasons = {None: []}

	for episode in (f for f in os.listdir(show_path) if not f.startswith('.')):

		info = re.findall(r'\d+', os.path.splitext(episode)[0])
		episode_path = os.path.join(str(tv_dir['id']), show, episode)

		if not info or len(info) != 2:
			seasons[None].append((None, episode_path))
		else:

			try:
				seasons[info[0]].append((info[1], episode_path))
			except KeyError:
				seasons[info[0]] = [(info[1], episode_path)]

	return seasons


def _read_shows(tv_dir):

	"""Builds a list of TV shows."""

	tv_shows = []
	tv_path = tv_dir['path']

	for name in (show for show in os.listdir(tv_path) if _is_dir(tv_path, show)):

		show_name = name.replace('_', ' ').title()

		show_entry = {'name': show_name, 'dirname': name}
		show_entry['seasons'] = _get_seasons(tv_dir, name)

		tv_shows.append(show_entry)

	return tv_shows


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


def _shows_to_delete(db, show_dirs):

	"""Compares shows on disk to those stored in the database, and returns
	list of shows to be deleted."""

	db_shows = db.query('SELECT dirname, id FROM tv_shows')
	stored_shows = {show['dirname']: show['id'] for show in db_shows}

	shows_delete = []

	for show, show_id in stored_shows.items():

		if show not in show_dirs:
			shows_delete.append((show_id,))

	return shows_delete


def _get_show(db, name, dirname):

	"""Retrieves or insert a show into the database, returns the id."""

	result = db.query('SELECT id FROM tv_shows WHERE dirname = ?', (dirname,))
	show_id = result[0]['id'] if result else result

	if not show_id:

		show_id = db.query('INSERT INTO tv_shows (name, dirname) VALUES (?, ?)',
			(name, dirname))

	return show_id


def _diff_episodes(db, show, current_episodes):

	"""For a particular show, returns episodes to be added."""

	to_add = []
	show_id = _get_show(db, show['name'], show['dirname'])

	for season_num, season in show['seasons'].items():

		for episode in season:

			exists = current_episodes.pop(episode[1], None)

			if not exists:
				to_add.append((episode[0], season_num, episode[1], show_id))

	return to_add


def _diff_shows(db, tv_dir, current_episodes):

	"""Returns a list of episodes to be added, and another of the ids of those
	to be deleted, and a third with a list of shows to be deleted."""

	to_add = []
	shows = _read_shows(tv_dir)

	for show in shows:
		to_add += _diff_episodes(db, show, current_episodes)

	to_delete = ((episode,) for episode in current_episodes.values())
	shows_delete = _shows_to_delete(db, {show['dirname'] for show in shows})

	return to_add, to_delete, shows_delete


def _sync_movies(db, movie_dir):

	"""Dummy function for synchronising movies."""

	db_movies = db.query('SELECT path, id FROM movies')
	stored_movies = {movie['path']: movie['id'] for movie in db_movies}

	movies_add, movies_delete = _diff_movies(movie_dir, stored_movies)

	db.many('INSERT INTO movies (name, path) VALUES (?, ?)', movies_add)
	db.many('DELETE FROM movies WHERE id = ?', movies_delete)


def _sync_shows(db, tv_dir):

	"""Dummy function for synchronising TV shows."""

	db_episodes = db.query('SELECT path, id FROM episodes')
	stored_episodes = {ep['path']: ep['id'] for ep in db_episodes}

	eps_add, eps_delete, shows_delete = _diff_shows(db, tv_dir, stored_episodes)

	db.many("""INSERT INTO episodes (number, season, path, show)
		VALUES (?, ?, ?, ?)""", eps_add)
	db.many('DELETE FROM episodes WHERE id = ?', eps_delete)
	db.many('DELETE FROM tv_shows WHERE id = ?', shows_delete)


def sync(db_file):

	"""Synchronises the database with the files on disk."""

	if db_file:

		db = Database(db_file)
		media_locations = db.query('SELECT * FROM media_locations')

		for location in media_locations:

			if location['type'] == 'movies':
				_sync_movies(db, location)
			elif location['type'] == 'tv_shows':
				_sync_shows(db, location)

	else:
		raise Exception('No db file given.')
