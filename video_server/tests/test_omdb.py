# ----- Imports ----- #

import unittest
import video_server.omdb as omdb


# ----- Tests ----- #

class TestOmdb(unittest.TestCase):

	"""Tests the omdb.py module."""

	def test_movie_data(self):

		"""Makes sure movie data is retrieved correctly."""

		data = omdb._movie_data('Big Buck Bunny')
		self.assertTrue(all(field in data for field in omdb._MOVIE_FIELDS))
		self.assertEqual(data.imdb_id, 'tt1254207')

	def test_show_data(self):

		"""Makes sure show data is retrieved correctly."""

	def test_ep_data(self):

		"""Makes sure episode data is retrieved correctly."""
