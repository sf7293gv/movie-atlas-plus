import sqlite3
from .config import db_path
from model.movie_model import Favorite

db = db_path

class FavoritesDB():
    
    def __init__(self):
        #create table function
        with sqlite3.connect(db) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS favorites (
                        tmdb_id TEXT NOT NULL UNIQUE, 
                        title TEXT NOT_NULL,
                        director TEXT,
                        release_date TEXT,
                        actor_1 TEXT,
                        actor_2 TEXT,
                        poster_img TEXT,
                        genre TEXT,
                        rating TEXT,
                        plot_summary TEXT,
                        youtube_video_title TEXT,
                        youtube_id TEXT)"""
                        )

        # conn.close()    


    # fetch all favorite movies from db
    def get_all_favorites(self):

        with sqlite3.connect(db) as conn:
            try:
                conn.row_factory = sqlite3.Row
                results_query = conn.execute(f'SELECT * FROM favorites')
                all_favorites = results_query.fetchall()
                
                return all_favorites
            except Exception as e:
                return None, 'Error getting all favorites because ' + str(e)
                
    # add movie to favorites db
    def add_favorite(self, movie):
        with sqlite3.connect(db) as conn:
            try:
                conn.execute(f'INSERT INTO favorites VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            (movie.tmdb_id,
                            movie.title,
                            movie.director,
                            movie.release_date,
                            movie.actor_1,
                            movie.actor_2,
                            movie.poster_img,
                            movie.genre,
                            movie.rating,
                            movie.plot_summary,
                            movie.youtube_video_title,
                            movie.youtube_id))
                
            except Exception as e:
                return 'Error adding favorite to db because ' + str(e)
    
    def delete_favorite(self, tmdb_id):
        
        with sqlite3.connect(db) as conn:
            try:
                conn.row_factory = sqlite3.Row
                conn.execute('DELETE FROM favorites WHERE tmdb_id = ?', (tmdb_id,))

            except Exception as e:
                return None, 'Error deleting movie from Favorites db because ' + str(e)   
    
    def get_one_favorite(self, tmdb_id):
        # check if movie title selected is already in db, return whole movie object if it is
        with sqlite3.connect(db) as conn:
            try:
                conn.row_factory = sqlite3.Row
                results_query = conn.execute('SELECT * FROM favorites WHERE tmdb_id = ?', (tmdb_id,))
                results = results_query.fetchone()
                if results == None:
                    return None # or return False/True
                else:
                    requested_movie = Favorite(results[0],
                                            results[1],
                                            results[2],
                                            results[3],
                                            results[4],
                                            results[5],
                                            results[6],
                                            results[7],
                                            results[8],
                                            results[9],
                                            results[10],
                                            results[11]
                                            )
                    return requested_movie
            except Exception as e:
                return None, 'Error getting favorite from database because ' + str(e)
                