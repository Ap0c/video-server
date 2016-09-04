# ----- Imports ----- #

import omdb


# ----- Setup ----- #

_MOVIE_FIELDS = ('poster_url', 'plot', 'runtime', 'year', 'imdb_rating',
	'actors', 'director')
_SHOW_FIELDS = ('poster_url', 'year', 'plot')
_EP_FIELDS = ('poster_url', 'plot', 'runtime', 'title')


# ----- Functions ----- #

def _movie_data(name):

	"""Retrieves the info for a movie by name."""

	metadata = omdb.get(title=name)
	return {f: metadata[f] for f in _MOVIE_FIELDS if f in metadata}


def _show_data(name):

	"""Retrieves the info for a show by name."""

	metadata = omdb.get(title=name)
	return {f: metadata[f] for f in _SHOW_FIELDS if f in metadata}


def _ep_data(show=None, season=None, episode=None):

	"""Retrieves the info for an episode."""

	metadata = omdb.get(title=show, season=season, episode=episode)
	return {f: metadata[f] for f in _EP_FIELDS if f in metadata}


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
