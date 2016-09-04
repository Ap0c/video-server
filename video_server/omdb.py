# ----- Imports ----- #

import omdb


# ----- Setup ----- #

_MOVIE_FIELDS = ('poster_url', 'plot', 'runtime', 'year', 'imdb_rating',
	'actors', 'director')
_SHOW_FIELDS = ()
_EP_FIELDS = ()


# ----- Functions ----- #

def _movie_data(name):

	"""Retrieves the info for a movie by name."""

	metadata = omdb.get(title=name)
	return {field: metadata[field] for field in _MOVIE_FIELDS if field in metadata}

def _show_data(name):

	"""Retrieves the info for a show by name."""

def _ep_data(show=None, season=None, episode=None):

	"""Retrieves the info for an episode."""
