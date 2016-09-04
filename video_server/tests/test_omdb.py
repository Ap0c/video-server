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

		data = omdb._ep_data(show='Silicon Valley', season=1, episode=1)
		self.assertIn('title', data)

	def test_lookup_movies(self):

		"""Makes sure list of movies is retrieved correctly."""

		movies = [{'id': 1, 'name': 'Big Buck Bunny'}]
		metadata = omdb._lookup_movies(movies)

		self.assertEqual(metadata[0]['year'], '2008')
		self.assertEqual(metadata[0]['id'], 1)
