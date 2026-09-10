"""
VISTOR Documentary
"""

from __future__ import annotations

from metadata.media.media_item import MediaItem


class Documentary(MediaItem):
    """Represents a documentary film or television documentary."""

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

        self.subject: str = ""

        self.narrator: str = ""

        self.series_name: str = ""

        self.episode_title: str = ""

        self.is_feature_length = False

    # ------------------------------------------------------------------
    # Subject
    # ------------------------------------------------------------------

    def get_subject(self):
        """Return the documentary subject."""

        return self.subject

    def set_subject(self, subject: str):
        """Set the documentary subject."""

        self.subject = subject

    # ------------------------------------------------------------------
    # Narrator
    # ------------------------------------------------------------------

    def get_narrator(self):
        """Return the narrator."""

        return self.narrator

    def set_narrator(self, narrator: str):
        """Set the narrator."""

        self.narrator = narrator

    # ------------------------------------------------------------------
    # Series Information
    # ------------------------------------------------------------------

    def get_series_name(self):
        """Return the documentary series name."""

        return self.series_name

    def set_series_name(self, name: str):
        """Set the documentary series name."""

        self.series_name = name

    def get_episode_title(self):
        """Return the documentary episode title."""

        return self.episode_title

    def set_episode_title(self, title: str):
        """Set the documentary episode title."""

        self.episode_title = title

    # ------------------------------------------------------------------
    # Runtime
    # ------------------------------------------------------------------

    def is_feature_documentary(self):
        """Return whether this is feature length."""

        return self.is_feature_length

    def set_feature_length(self, feature: bool):
        """Set whether this is feature length."""

        self.is_feature_length = feature

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self):
        return self.title
