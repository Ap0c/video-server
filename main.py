# ----- Imports ----- #

from flask import Flask, render_template


# ----- Setup ----- #

app = Flask(__name__)


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
	app.run(debug=True)
