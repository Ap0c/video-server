# ----- Setup ----- #

MEDIA_TYPES = ['movie', 'show', 'episode']
_EDITABLE_FIELDS = ['name', 'number', 'season']
_FIELD_TYPES = {
	'name': 'text',
	'number': 'number',
	'season': 'number'
}


# ----- Functions ----- #

def _query_db(db, media_id, media_type):

	"""Constructs a query and executes it based upon the media info."""

	if media_type == 'movie':
		query = 'SELECT name, path FROM movies WHERE id=?'
	elif media_type == 'show':
		query = 'SELECT name, dirname FROM tv_shows WHERE id=?'
	elif media_type == 'episode':
		query = 'SELECT name, number, season, path FROM episodes WHERE id=?'

	return db.query(query, (media_id,))


def _metadata_fields(field_name, value):

	"""Returns the formatted metadata along with additional information."""

	formatted = {
		'field': field_name,
		'value': value.split('/', 1)[1] if field_name == 'path' else value,
		'editable': True if field_name in _EDITABLE_FIELDS else False
	}

	if formatted['editable']:
		formatted['type'] = _FIELD_TYPES[field_name]

	return formatted


def get_metadata(db, media_id, media_type):

	"""Retrieves metadata from the database and formats it."""

	stored_metadata = _query_db(db, media_id, media_type)

	if not stored_metadata:
		return None

	metadata = []

	for key, value in dict(stored_metadata[0]).items():
		metadata.append(_metadata_fields(key, value))

	return metadata
