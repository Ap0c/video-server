# ----- Imports ----- #

import sqlite3


# ----- Database Class ----- #

class db():

	"""An object for managing database connections and queries."""

	def __init__(self, db_file):

		self.db_file = db_file

	def _connection(self, func):

		"""Decorator to open and close a database connection."""

		def wrapper(*args, **kwargs):

			self.conn = sqlite3.connect(self.db_file)
			self.conn.row_factory = sqlite3.Row
			self.cursor = self.conn.cursor()

			result = func(*args, **kwargs)

			self.conn.commit()
			self.conn.close()
			self.conn = None
			self.cur = None

			return result

		return wrapper

	@_connection
	def query(self, querystring, args=()):

		"""Query the database with a querystring and args."""

		self.cur.execute(querystring, args)
		row_id = self.cur.lastrowid

		return row_id or self.cur.fetchall()
