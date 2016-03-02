# ----- Imports ----- #

from flask import Flask, g, render_template, request
from threading import Thread
import os.path
import subprocess

from .scan import sync
from .db import Database


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


# ----- Setup ----- #

# The app object.
app = Flask(__name__)

# Handles database connections and queries.
db = Database(DB_FILE, DB_SCHEMA)


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

	info = db.query('SELECT * FROM movies WHERE id = ?', (movie_id,), True)
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

	info = db.query('SELECT * FROM tv_shows WHERE id = ?', (show_id,), True)
	episodes = db.query('SELECT * FROM episodes WHERE show = ?', (show_id,))

	return render_template('show.html', name=info['name'], episodes=episodes)


@app.route('/tv_shows/episode/<episode_id>')
def episode(episode_id):

	"""Displays an episode page."""

	info = db.query('SELECT * FROM episodes WHERE id = ?', (episode_id,), True)
	show = db.query('SELECT * FROM tv_shows WHERE id = ?',
		(info['show'],), True)

	video_url = '/{}/{}'.format(MEDIA_URL, info['path'])

	return render_template('episode.html', episode=info, show=show,
		video_url=video_url)


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

		symlink_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
			MEDIA_DIR, str(row_id))
		subprocess.call(['ln', '-s', media_path, symlink_path])

		return 'Created', 201

	else:
		return 'No such path on the file system.', 400
