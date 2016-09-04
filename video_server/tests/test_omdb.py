# ----- Imports ----- #

import unittest
import video_server.omdb as omdb


# ----- Tests ----- #

class TestOmdb(unittest.TestCase):

	"""Tests the omdb.py module."""

	def test_movie_data(self):

		"""Makes sure movie data is retrieved correctly."""

		data = omdb._movie_data('Big Buck Bunny')
		self.assertEqual(data['year'], '2008')

	def test_show_data(self):

		"""Makes sure show data is retrieved correctly."""

		data = omdb._show_data('Silicon Valley')
		self.assertIn('year', data)

	def test_ep_data(self):

		"""Makes sure episode data is retrieved correctly."""

		data = omdb._show_data(show='Silicon Valley', season=1, episode=1)
		self.assertEqual(data.imdb_id, 'tt3222784')
