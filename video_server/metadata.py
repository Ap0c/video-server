# ----- Setup ----- #

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


def _validate_fields(new_data):

	"""Checks that new data is of the correct format."""

	for field, field_type in _FIELD_TYPES.items():

		if field in new_data and field_type == 'number':

			try:
				int(new_data[field])
			except ValueError:
				return False, "The field '{}' must be an integer.".format(field)

	return True, None


def get_metadata(db, media_id, media_type):

	"""Retrieves metadata from the database and formats it."""

	stored_metadata = _query_db(db, media_id, media_type)

	if not stored_metadata:
		return None

	metadata = []

	for key, value in dict(stored_metadata[0]).items():
		metadata.append(_metadata_fields(key, value))

	return metadata


def update_metadata(db, media_id, media_type, new_data):

	"""Updates the metadata in the database."""

	valid, err = _validate_fields(new_data)

	if not valid:
		return False, err

	if media_type == 'movie':

		query = 'UPDATE movies SET name=? WHERE id=?'
		args = (new_data['name'], media_id)

	elif media_type == 'show':

		query = 'UPDATE tv_shows SET name=? WHERE id=?'
		args = (new_data['name'], media_id)

	elif media_type == 'episode':

		query = 'UPDATE episodes SET name=?, number=?, season=? WHERE id=?'
		args = (new_data['name'], new_data['number'], new_data['season'], media_id)

	db.query(query, args)
	return True, None
