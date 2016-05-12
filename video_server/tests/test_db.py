# ----- Imports ----- #

import unittest
from video_server.db import Database


# ----- Tests ----- #

class TestDb(unittest.TestCase):

	"""Tests the db.py module."""

	def test_instantiate(self):

		"""Makes sure the db instantiates without error."""

		db = Database('test.db')
