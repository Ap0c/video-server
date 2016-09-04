CREATE TABLE IF NOT EXISTS movies
	(id INTEGER PRIMARY KEY, name TEXT, path TEXT);

CREATE TABLE IF NOT EXISTS tv_shows
	(id INTEGER PRIMARY KEY, name TEXT, dirname TEXT);

CREATE TABLE IF NOT EXISTS episodes
	(id INTEGER PRIMARY KEY, name TEXT, number INTEGER, season INTEGER,
		path TEXT, show INTEGER,
		FOREIGN KEY (show) REFERENCES show(id));

CREATE TABLE IF NOT EXISTS media_locations
	(id INTEGER PRIMARY KEY, type TEXT, path TEXT UNIQUE
		CONSTRAINT check_type CHECK (type IN ('movies', 'tv_shows')));

CREATE TABLE IF NOT EXISTS movie_metadata
	(id INTEGER PRIMARY KEY, poster_url TEXT, plot TEXT, runtime TEXT,
		year TEXT, imdb_rating TEXT, actors TEXT, director TEXT,
		FOREIGN KEY (id) REFERENCES movies(id));

CREATE TABLE IF NOT EXISTS show_metadata
	(id INTEGER PRIMARY KEY, poster_url TEXT, plot TEXT, year TEXT,
		FOREIGN KEY (id) REFERENCES tv_shows(id));

CREATE TABLE IF NOT EXISTS episode_metadata
	(id INTEGER PRIMARY KEY, poster_url TEXT, plot TEXT, runtime TEXT,
		title TEXT,
		FOREIGN KEY (id) REFERENCES episodes(id));
