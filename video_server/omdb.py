# ----- Imports ----- #

import omdb
from .db import Database


# ----- Setup ----- #

_MOVIE_FIELDS = ('poster_url', 'plot', 'runtime', 'year', 'imdb_rating',
	'actors', 'director')
_SHOW_FIELDS = ('poster_url', 'year', 'plot')
_EP_FIELDS = ('poster_url', 'plot', 'runtime', 'title')


# ----- Functions ----- #

def _movie_data(name):

	"""Retrieves the info for a movie by name."""

	metadata = omdb.get(title=name)
	return {f: (metadata[f] if f in metadata else None) for f in _MOVIE_FIELDS}


def _show_data(name):

	"""Retrieves the info for a show by name."""

	metadata = omdb.get(title=name)
	return {f: (metadata[f] if f in metadata else None) for f in _SHOW_FIELDS}


def _ep_data(show=None, season=None, episode=None):

	"""Retrieves the info for an episode."""

	metadata = omdb.get(title=show, season=season, episode=episode)
	return {f: (metadata[f] if f in metadata else None) for f in _EP_FIELDS}


def _lookup_movies(movies):

	"""Looks up movie metadata."""

	result = []

	for movie in movies:

		metadata = _movie_data(movie['name'])
		metadata['id'] = movie['id']

		result.append(metadata)

	return result


def _lookup_shows(shows):

	"""Looks up show metadata."""

	result = []

	for show in shows:

		metadata = _show_data(show['name'])
		metadata['id'] = show['id']

		result.append(metadata)

	return result


def _lookup_eps(episodes):

	"""Looks up episode metadata."""

	result = []

	for episode in episodes:

		metadata = _ep_data(show=episode['show'], season=episode['season'],
			episode=episode['number'])
		metadata['id'] = episode['id']

		result.append(metadata)

	return result


def _scrape_movies(db):

	"""Retrieves movies, looks up metadata, and stores it in the db."""

	movies = db.query('SELECT id, name FROM movies')
	query = 'INSERT INTO movie_metadata VALUES ({})'.format(
		','.join(['?']*len(movies))
	)

	db.many(query, movies)


def _scrape_shows(db):

	"""Retrieves shows, looks up metadata, and stores it in the db."""

	shows = db.query('SELECT id, name FROM tv_shows')
	query = 'INSERT INTO show_metadata VALUES ({})'.format(
		','.join(['?']*len(shows))
	)

	db.many(query, shows)


def _scrape_eps(db):

	"""Retrieves episodes, looks up metadata, and stores it in the db."""

	episodes = db.query("""SELECT episodes.id AS id, episodes.number AS number,
		episodes.season AS season, tv_shows.name AS show
			FROM episodes, tv_shows
			WHERE tv_shows.id = episodes.show""")

	query = 'INSERT INTO episode_metadata VALUES ({})'.format(
		','.join(['?']*len(episodes))
	)

	db.many(query, episodes)


def lookup_media(db_file):

	"""Retrieves the metadata for media in a database, and stores it."""

	if db_file:

		db = Database(db_file)
		_scrape_movies(db)
		_scrape_shows(db)
		_scrape_eps(db)

	else:
		raise Exception('No db file given.')
