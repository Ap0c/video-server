# ----- Imports ----- #

import omdb


# ----- Setup ----- #

_MOVIE_FIELDS = ('poster_url', 'plot', 'runtime', 'year', 'imdb_rating',
	'actors', 'director')
_SHOW_FIELDS = ('poster_url', 'year', 'plot')
_EP_FIELDS = ()


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
