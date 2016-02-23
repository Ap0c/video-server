# ----- Imports ----- #

from flask import Flask


# ----- Setup ----- #

app = Flask(__name__)


# ----- Routes ----- #

@app.route('/')
def index():

	"""Displays the homepage."""

	return 'Hello world'


# ----- Main ----- #

if __name__ == '__main__':
	app.run(debug=True)
