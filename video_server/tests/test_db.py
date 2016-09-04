# ----- Imports ----- #

import unittest
import os
from video_server.db import Database
from nose.tools import nottest


# ----- Setup ----- #

SCHEMA_FILE = 'video_server/schema.sql'
TEST_DB = 'test.db'


# ----- Tests ----- #

@nottest
class TestDb(unittest.TestCase):

	"""Tests the db.py module."""

	def test_instantiate(self):

		"""Db instantiates without error."""

		db = Database(TEST_DB)
		db = Database(TEST_DB, SCHEMA_FILE)

	def test_query_select(self):

		"""SELECT query runs without error."""

		db = Database(TEST_DB, SCHEMA_FILE)

		result = db.query('SELECT * FROM movies')
		self.assertEqual(result, [])

	def test_query_insert(self):

		"""INSERT query runs without error."""

		db = Database(TEST_DB, SCHEMA_FILE)

		args = ('Dummy Movie', 'dummy/path')
		result = db.query('INSERT INTO movies (name, path) VALUES (?, ?)', args)
		self.assertEqual(result, 1)

		row = db.query('SELECT * FROM movies')[0]
		self.assertEqual(row['name'], args[0])
		self.assertEqual(row['path'], args[1])

	def tearDown(self):

		"""Removes any instance of the test database."""

		os.remove(TEST_DB)
