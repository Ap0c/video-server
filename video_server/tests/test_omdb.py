# ----- Imports ----- #

import unittest
import video_server.omdb as omdb


# ----- Tests ----- #

class TestOmdb(unittest.TestCase):

	"""Tests the omdb.py module."""

	def test_movie_data(self):

		"""Makes sure movie data is retrieved correctly."""

		data = omdb._movie_data('Big Buck Bunny')

		self.assertTrue(all(k in data for k in omdb._MOVIE_FIELDS))
		self.assertEqual(data['year'], '2008')

	def test_show_data(self):

		"""Makes sure show data is retrieved correctly."""

		data = omdb._show_data('Silicon Valley')

		self.assertTrue(all(k in data for k in omdb._SHOW_FIELDS))
		self.assertIn('year', data)

	def test_ep_data(self):

		"""Makes sure episode data is retrieved correctly."""

		data = omdb._ep_data(show='Silicon Valley', season=1, episode=1)

		self.assertTrue(all(k in data for k in omdb._EP_FIELDS))
		self.assertIn('title', data)

	def test_lookup_movies(self):

		"""Makes sure list of movies is retrieved correctly."""

		movies = [{'id': 1, 'name': 'Big Buck Bunny'}]
		metadata = omdb._lookup_movies(movies)

		self.assertEqual(metadata[0]['year'], '2008')
		self.assertEqual(metadata[0]['id'], 1)

	def test_lookup_shows(self):

		"""Makes sure list of shows is retrieved correctly."""

		shows = [{'id': 2, 'name': 'Silicon Valley'}]
		metadata = omdb._lookup_shows(shows)

		self.assertIn('year', metadata[0])
		self.assertEqual(metadata[0]['id'], 2)

	def test_lookup_eps(self):

		"""Makes sure list of shows is retrieved correctly."""

		episodes = [{'id': 3, 'show': 'Silicon Valley', 'season': 1, 'number': 1}]
		metadata = omdb._lookup_eps(episodes)

		self.assertIn('title', metadata[0])
		self.assertEqual(metadata[0]['id'], 3)
