# ----- Imports ----- #

from flask import Flask, g, render_template, request, redirect, url_for
from threading import Thread
import os

from .scan import sync
from .db import Database
import video_server.metadata as mdata


# ----- Constants ----- #

# The database schema file.
DB_SCHEMA = os.path.join(os.path.dirname(os.path.realpath(__file__)),
	'schema.sql')

# The database file.
DB_FILE = 'media.db'

# Location of the app media directory.
MEDIA_DIR = 'media'

# Media url.
MEDIA_URL = 'media'

# Possible media types.
MEDIA_TYPES = ['movie', 'show', 'episode']

# Current working directory.
WORKING_DIR = os.getcwd()


# ----- Setup ----- #

# The app object.
app = Flask(__name__)

# Handles database connections and queries.
db = Database(DB_FILE, DB_SCHEMA)

# Creates the media directory.
if not os.path.exists(MEDIA_DIR):
	os.mkdir(MEDIA_DIR)


# ----- Functions ----- #

def _metadata_redirect(media_id, media_type):

	"""Parameters for redirect after updating metadata."""

	if media_type == 'movie':

		route = 'movie'
		route_args = {'movie_id': media_id}

	elif media_type == 'show':

		route = 'tv_show'
		route_args = {'show_id': media_id}

	elif media_type == 'episode':

		route = 'episode'
		route_args = {'episode_id': media_id}

	return route, route_args


# ----- Routes ----- #

@app.route('/')
def index():

	"""Displays the homepage."""

	return render_template('index.html')


@app.route('/movies')
def movies():

	"""Displays a list of movies."""

	movie_list = db.query('SELECT * FROM movies')

	return render_template('movies.html', movies=movie_list)


@app.route('/movies/<movie_id>')
def movie(movie_id):

	"""Displays a movie page."""

	info = db.query('SELECT * FROM movies WHERE id = ?', (movie_id,))[0]
	video_url = '/{}/{}'.format(MEDIA_URL, info['path'])

	return render_template('movie.html', movie=info, video_url=video_url)


@app.route('/tv_shows')
def tv_shows():

	"""Displays a list of TV shows."""

	show_list = db.query('SELECT * FROM tv_shows')

	return render_template('tv_shows.html', shows=show_list)


@app.route('/tv_shows/show/<show_id>')
def tv_show(show_id):

	"""Displays a TV show page."""

	info = db.query('SELECT * FROM tv_shows WHERE id = ?', (show_id,))[0]
	episodes = db.query('SELECT * FROM episodes WHERE show = ?', (show_id,))
	unknown_season = None in (episode['season'] for episode in episodes)

	return render_template('show.html', show=info, episodes=episodes,
		unknown_season=unknown_season)


@app.route('/tv_shows/episode/<episode_id>')
def episode(episode_id):

	"""Displays an episode page."""

	info = db.query('SELECT * FROM episodes WHERE id = ?', (episode_id,))[0]
	show = db.query('SELECT * FROM tv_shows WHERE id = ?', (info['show'],))[0]

	video_url = '/{}/{}'.format(MEDIA_URL, info['path'])

	return render_template('episode.html', episode=info, show=show,
		video_url=video_url)


@app.route('/edit_metadata/<media_type>/<media_id>', methods=['GET', 'POST'])
def edit_metadata(media_type, media_id):

	"""View for editing metadata, and endpoint for posting the edited data."""

	error = None

	if media_type not in MEDIA_TYPES:
		return 'Media type not recognised.', 404

	# POST requests.
	if request.method == 'POST':

		form = request.form
		valid, error = mdata.update_metadata(db, media_id, media_type, form)

		if valid:

			route, route_args = _metadata_redirect(media_id, media_type)
			return redirect(url_for(route, **route_args))

	# GET requests and failed POST requests.
	metadata = mdata.get_metadata(db, media_id, media_type)

	if not metadata:
		return 'Media ID not recognised.', 404

	return render_template('edit_metadata.html', metadata=metadata,
		media_type=media_type, error=error)


@app.route('/settings')
def settings():

	"""Displays the settings page."""

	locations = db.query('SELECT * FROM media_locations')

	return render_template('settings.html', locations=locations)


@app.route('/scan', methods=['POST'])
def scan():

	"""Starts thread to scan media directories and populate database."""

	scan_thread = getattr(g, '_scan_thread', None)

	if not scan_thread or not scan_thread.isAlive():
		g._scan_thread = Thread(target=sync, args=(DB_FILE,))
		g._scan_thread.start()

	return 'Accepted', 202


@app.route('/add_source', methods=['PUT'])
def add_source():

	"""Adds a new media source to the database."""

	media_type = request.form['source-type']
	media_path = request.form['source-path']

	if (os.path.isdir(media_path)):

		row_id = db.query('INSERT INTO media_locations (type, path) VALUES (?, ?)',
			(media_type, media_path))

		symlink_path = os.path.join(WORKING_DIR, MEDIA_DIR, str(row_id))
		os.symlink(media_path, symlink_path)

		return 'Created', 201

	else:
		return 'No such path on the file system.', 400
