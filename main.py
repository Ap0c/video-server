# ----- Imports ----- #

from flask import Flask, render_template


# ----- Setup ----- #

app = Flask(__name__)


# ----- Routes ----- #

@app.route('/')
def index():

	"""Displays the homepage."""

	return render_template('index.html')


# ----- Main ----- #

if __name__ == '__main__':
	app.run(debug=True)
