# ----- Imports ----- #

from flask import Flask, g, render_template
import sqlite3


# ----- Constants ----- #

# The database schema file.
DB_SCHEMA = 'schema.sql'

# The database file.
DB_FILE = 'media.db'


# ----- Setup ----- #

# The app object.
app = Flask(__name__)


# ----- Functions ----- #

def get_db():

	"""Retrieves a database connection."""

	db = getattr(g, '_database', None)

	if db is None:

		db = g._database = sqlite3.connect(DB_FILE)
		db.row_factory = sqlite3.Row

	return db


@app.teardown_appcontext
def close_connection(exception):

	"""Closes the database connection when app context is destroyed."""

	db = getattr(g, '_database', None)

	if db is not None:
		db.close()


def query_db(query, args=(), single_result=False):

	"""Queries the database."""

	cur = get_db().execute(query, args)

	results = cur.fetchall()
	cur.close()

	return (results[0] if results else None) if single_result else results


def init_db():

	"""Creates the database from a schema file."""

	with app.app_context():

		db = get_db()

		with app.open_resource(DB_SCHEMA, mode='r') as schema_file:
			db.cursor().executescript(schema_file.read())

		db.commit()


# ----- Routes ----- #

@app.route('/')
def index():

	"""Displays the homepage."""

	return render_template('index.html')


@app.route('/movies')
def movies():

	"""Displays a list of movies."""

	return render_template('movies.html')


@app.route('/tv_shows')
def tv_shows():

	"""Displays a list of tv shows."""

	return render_template('tv_shows.html')


# ----- Main ----- #

if __name__ == '__main__':

	init_db()
	app.run(debug=True)
