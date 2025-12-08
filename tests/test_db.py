import sqlite3
import unittest
from unittest import TestCase 
from database import cached_db
from datetime import datetime, date, time
from exceptions.movie_error import MovieError


class TestCacheDatbase(TestCase):

    # create test db
    test_cache_db = 'test_cache_db.sqlite'

    def setUp(self):
        # set up the test db (delete from previous test)
        cached_db.db = self.test_cache_db

        with sqlite3.connect(self.test_cache_db) as conn:
            conn.execute('DROP TABLE IF EXISTS movies_cache')
        conn.close()

        with sqlite3.connect(self.test_cache_db) as conn:
            conn.execute("""CREATE TABLE movies_cache (
                            title TEXT NOT_NULL,
                            release_year TEXT,
                            tmdb_id TEXT NOT NULL,
                            time_cached INTEGER NOT NULL)"""
                        )
        conn.close()

        self.db = cached_db.CacheDB()

    def test_add_movie_list_cache_adds_list(self):
        test_movie_1 = [{'title':'First Movie', 'release_year':'2020', 'tmdb_id':123456}]
        self.db.add_movie_list_cache(test_movie_1)
        expected = [{'title':'First Movie', 'release_year':'2020', 'tmdb_id':123456}]
        self.compare_db_to_expected(expected)
        
        test_movie_2 = [{'title':'Second Movie', 'release_year':'1990', 'tmdb_id':654321}]
        self.db.add_movie_list_cache(test_movie_2)
        expected = [{'title':'Second Movie', 'release_year':'1990', 'tmdb_id':654321, 'time_cached':datetime.now().timestamp()}]
        self.compare_db_to_expected(expected)

    def test_add_movie_not_add_duplicate(self):
        test_movie = [{'title':'Unique Movie', 'release_year':'2020', 'tmdb_id':987654}]
        self.db.add_movie_list_cache(test_movie)
        expected = [{'title':'Unique Movie', 'release_year':'2020', 'tmdb_id':987654, 'time_cached':datetime.now().timestamp()}]
        self.compare_db_to_expected(expected)

        with self.assertRaises(MovieError):
            test_movie_2 = [{'title':'Duplicate Movie', 'release_year':'2020', 'tmdb_id':987654}]
            self.db.add_movie_list_cache(test_movie_2)

    def test_check_cache_expired_clears_cache_returns_none(self):
        test_movie = [{'title':'Clear Movie', 'release_year':'2010', 'tmdb_id':345678}]
        self.db.add_movie_list_cache(test_movie)
        time.sleep(cached_db.MAX_AGE_SECONDS + 10) # pause program from initial add for amount of time greater than MAX_AGE_SECONDS variable
        self.db.check_cache() # need to figure out what to test. Maybe that it returns None?
        # use helper method to query db and return what should be None because cache was cleared
        expected = {}
        self.compare_db_to_expected(expected)
        # may need to add single movie after this and we should only get that movie, or maybe readd the movie from the 
        # first line of the function and we should not get an error back

    def test_check_cache_returns_movies_list(self):
        test_movies = [{'title':'Cache Movie', 'release_year':'2012', 'tmdb_id':234567},
                        {'title':'Cache Movie 2', 'release_year':'2015', 'tmdb_id':345867}]
        self.db.add_movie_list_cache(test_movies)
        checked_cache_test = self.db.check_cache()
        self.compare_db_to_expected(checked_cache_test)

    def compare_db_to_expected(self, expected):

        conn = sqlite3.connect(self.test_cache_db)
        all_rows = conn.execute('SELECT * FROM movies_cache').fetchall()

        self.assertEqual(len(expected.keys()), len(all_rows))

        for row in all_rows:
            self.assertIn(row[0], expected.keys())
            self.assertEqual(expected[row[0]], row[1])
        
        conn.close()