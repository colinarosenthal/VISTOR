"""
VISTOR Music Video
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from metadata.media.media_item import MediaItem

if TYPE_CHECKING:
    from metadata.vocabulary.music_genre import MusicGenre


class MusicVideo(MediaItem):
    """Represents a broadcast music video."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        id: str,
        title: str,
        release_year: int = 0,
        runtime_minutes: int = 0,
    ):
        super().__init__(
            id=id,
            title=title,
            release_year=release_year,
            runtime_minutes=runtime_minutes,
        )

        self.song_title: str = title

        self.album: str = ""

        self.music_genre: MusicGenre | None = None

        self.record_label: str = ""

        self.director: str = ""

        self.chart_position: int | None = None

        self.is_live_performance = False

    # ------------------------------------------------------------------
    # Song
    # ------------------------------------------------------------------

    def get_song_title(self):
        """Return the song title."""

        return self.song_title

    def set_song_title(self, title: str):
        """Set the song title."""

        self.song_title = title

    def get_album(self):
        """Return the album."""

        return self.album

    def set_album(self, album: str):
        """Set the album."""

        self.album = album

    # ------------------------------------------------------------------
    # Genre
    # ------------------------------------------------------------------

    def get_music_genre(self):
        """Return the music genre."""

        return self.music_genre

    def set_music_genre(self, genre: MusicGenre):
        """Set the music genre."""

        self.music_genre = genre

    # ------------------------------------------------------------------
    # Production
    # ------------------------------------------------------------------

    def get_record_label(self):
        """Return the record label."""

        return self.record_label

    def set_record_label(self, label: str):
        """Set the record label."""

        self.record_label = label

    def get_director(self):
        """Return the music video director."""

        return self.director

    def set_director(self, director: str):
        """Set the music video director."""

        self.director = director

    # ------------------------------------------------------------------
    # Charts
    # ------------------------------------------------------------------

    def get_chart_position(self):
        """Return chart position."""

        return self.chart_position

    def set_chart_position(self, position: int):
        """Set chart position."""

        self.chart_position = position

    # ------------------------------------------------------------------
    # Broadcast
    # ------------------------------------------------------------------

    def is_live(self):
        """Return whether this is a live performance."""

        return self.is_live_performance

    def set_live(self, value: bool):
        """Set whether this is a live performance."""

        self.is_live_performance = value

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.song_title