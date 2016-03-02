# ----- Imports ----- #

import sqlite3


# ----- Functions ----- #

def _connection(func):

	"""Decorator to open and close a database connection."""

	def wrapper(*args, **kwargs):

		self = args[0]

		self.conn = sqlite3.connect(self.db_file)
		self.conn.row_factory = sqlite3.Row
		self.cur = self.conn.cursor()

		result = func(*args, **kwargs)

		self.conn.commit()
		self.conn.close()
		self.conn = None
		self.cur = None

		return result

	return wrapper


# ----- Database Class ----- #

class Database():

	"""An object for managing database connections and queries."""

	def __init__(self, db_file, schema_file=None):

		self.db_file = db_file

		if schema_file:
			self.init_db(schema_file)

	@_connection
	def init_db(self, schema_path):

		"""Sets up the database from a schema file."""

		with open(schema_path, 'r') as schema_file:
			self.cur.executescript(schema_file.read())

	@_connection
	def query(self, querystring, args=()):

		"""Query the database with a querystring and args."""

		self.cur.execute(querystring, args)
		row_id = self.cur.lastrowid

		return row_id or self.cur.fetchall()

	@_connection
	def many(self, querystring, args=()):

		"""Execute multiple queries on the database, will require args to be an
		iterable of tuples. Will not return anything."""

		self.cur.executemany(querystring, args)
