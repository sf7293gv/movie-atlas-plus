class Favorite():

    def __init__(self,
                tmdb_id,
                title,
                director,
                release_date,
                actor_1,
                actor_2,
                poster_img,
                genre,
                rating,
                plot_summary,
                youtube_video_title,
                youtube_id):
                
        self.tmdb_id = tmdb_id
        self.title = title
        self.director = director
        self.release_date = release_date
        self.actor_1 = actor_1
        self.actor_2 = actor_2
        self.poster_img = poster_img
        self.genre = genre
        self.rating = rating
        self.plot_summary = plot_summary
        self.youtube_video_title = youtube_video_title
        self.youtube_id = youtube_id
    
    def __str__(self):
        return f'{self.tmdb_id}, {self.title}, {self.director}, {self.release_date}, {self.actor_1}, {self.actor_2}, {self.poster_img}, {self.genre}, {self.rating}, {self.plot_summary}, {self.youtube_video_title}, {self.youtube_id}'