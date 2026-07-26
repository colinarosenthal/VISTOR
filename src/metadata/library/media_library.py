"""
VISTOR Media Library

Represents the complete metadata catalog known to VISTOR.

The MediaLibrary stores information about available programming
regardless of whether the physical media files currently exist locally.

It manages relationships between media objects but does not handle
file storage, downloading, or playback.
"""


class MediaLibrary:
    """Represents the VISTOR metadata catalog."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
    ):
        self.movies = []

        self.episodes = []

        self.sports_events = []

        self.sports_talk_shows = []

        self.music_videos = []
  
        self.commercials = []  

        self.concerts = []

        self.documentaries = []

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_movies(self):
        """Return all movies."""

        return self.movies

    def get_episodes(self):
        """Return all episodes."""

        return self.episodes

    def get_sports_events(self):
        """Return all sports events."""

        return self.sports_events

    def get_sports_talk_shows(self):
        """Return all sports talk shows."""

        return self.sports_talk_shows

    def get_music_videos(self):
        """Return all music videos."""

        return self.music_videos
    
    def get_commercials(self):  
        """Return all commercials."""  
  
        return self.commercials

    def get_concerts(self):
        """Return all concerts."""

        return self.concerts

    def get_documentaries(self):
        """Return all documentaries."""

        return self.documentaries

    # ------------------------------------------------------------------
    # Add Methods
    # ------------------------------------------------------------------

    def add_movie(self, movie):
        """Add a movie to the library."""

        self.movies.append(movie)

    def add_episode(self, episode):
        """Add an episode to the library."""

        self.episodes.append(episode)

    def add_sports_event(self, event):
        """Add a sports event to the library."""

        self.sports_events.append(event)

    def add_sports_talk_show(self, show):
        """Add a sports talk show."""

        self.sports_talk_shows.append(show)

    def add_music_video(self, video):
        """Add a music video."""

        self.music_videos.append(video)

    def add_commercial(self, commercial):  
        """Add a commercial to the library."""  
  
        self.commercials.append(commercial)

    def add_concert(self, concert):
        """Add a concert."""

        self.concerts.append(concert)

    def add_documentary(self, documentary):
        """Add a documentary."""

        self.documentaries.append(documentary)

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def get_total_media_count(self):
        """Return total number of media objects."""

        return (  
                len(self.movies)  
                + len(self.episodes)  
                + len(self.sports_events)  
                + len(self.sports_talk_shows)  
                + len(self.music_videos)  
                + len(self.commercials)  
                + len(self.concerts)  
                + len(self.documentaries)  
            )

    def __str__(self):
        return f"Media Library ({self.get_total_media_count()} items)"