"""
VISTOR Metadata Population Service

Creates default metadata objects used by VISTOR.
"""

from metadata.vocabulary.genre import Genre
from metadata.vocabulary.music_genre import MusicGenre
from metadata.vocabulary.theme import Theme


class MetadataPopulation:
    """
    Creates standardized metadata vocabulary.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # Genre Population
    # ------------------------------------------------------------------

    def create_genres(self):
        """
        Create default VISTOR media genres.
        """

        return [
            Genre(
                name="Action",
                description=(
                    "Programming centered around physical conflict, adventure, or high intensity events."
                ),
            ),
            Genre(
                name="Adventure",
                description="Programming focused on exploration, discovery, and journeys.",
            ),
            Genre(
                name="Animation",
                description="Animated television and film programming.",
            ),
            Genre(
                name="Comedy",
                description="Programming intended to entertain through humor.",
            ),
            Genre(
                name="Drama",
                description="Character-driven fictional storytelling.",
            ),
            Genre(
                name="Documentary",
                description="Non-fiction programming covering real subjects.",
            ),
            Genre(
                name="Horror",
                description=(
                    "Programming intended to create suspense, fear, or unsettling experiences."
                ),
            ),
            Genre(
                name="Science Fiction",
                description=(
                    "Stories involving science, technology, space, or future concepts."
                ),
            ),
            Genre(
                name="Fantasy",
                description="Stories involving magical or imaginary settings.",
            ),
            Genre(
                name="Reality",
                description="Unscripted programming featuring real people and events.",
            ),
            Genre(
                name="Sports",
                description="Competitive athletic programming.",
            ),
            Genre(
                name="News",
                description="Current events and informational programming.",
            ),
            Genre(
                name="Music",
                description="Music performances, videos, and related programming.",
            ),
        ]

    # ------------------------------------------------------------
    # Music Genre Population
    # ------------------------------------------------------------

    def create_music_genres(self):
        """
        Create default VISTOR music genres.
        """
        music_genres = []

        # ------------------------------------------------------------
        # Rock
        # ------------------------------------------------------------

        rock = MusicGenre(
            name="Rock",
            description="A broad genre centered around electric guitars, drums, and popular song structures.",
        )

        music_genres.append(rock)

        music_genres.extend([
            MusicGenre(
                name="Alternative Rock",
                description="Rock music associated with alternative and independent scenes.",
                parent_genre=rock,
            ),
            MusicGenre(
                name="Classic Rock",
                description="Rock music from influential 1960s through 1980s artists.",
                parent_genre=rock,
            ),
            MusicGenre(
                name="Hard Rock",
                description="A heavier rock style emphasizing powerful guitar riffs.",
                parent_genre=rock,
            ),
            MusicGenre(
                name="Glam Rock",
                description="Theatrical rock style known for visual presentation and performance.",
                parent_genre=rock,
            ),
            MusicGenre(
                name="Progressive Rock",
                description="Rock style featuring complex structures and experimental compositions.",
                parent_genre=rock,
            ),
            MusicGenre(
                name="Punk Rock",
                description="Fast and aggressive rock style associated with punk movements.",
                parent_genre=rock,
            ),
            MusicGenre(
                name="Indie Rock",
                description="Independent rock music emphasizing unique artistic approaches.",
                parent_genre=rock,
            ),
            MusicGenre(
                name="Grunge",
                description="Alternative rock movement associated with the Seattle music scene.",
                parent_genre=rock,
            ),
            MusicGenre(
                name="Pop Rock",
                description="Rock music incorporating accessible pop songwriting structures.",
                parent_genre=rock,
            ),
        ])

        # ------------------------------------------------------------
        # Metal
        # ------------------------------------------------------------

        metal = MusicGenre(
            name="Metal",
            description="A heavy music genre characterized by amplified guitars and aggressive performance.",
        )

        music_genres.append(metal)

        music_genres.extend([
            MusicGenre(
                name="Heavy Metal",
                description="Traditional metal style emphasizing powerful riffs and vocals.",
                parent_genre=metal,
            ),
            MusicGenre(
                name="Thrash Metal",
                description="Fast and aggressive metal style.",
                parent_genre=metal,
            ),
            MusicGenre(
                name="Death Metal",
                description="Extreme metal style featuring heavy distortion and harsh vocals.",
                parent_genre=metal,
            ),
            MusicGenre(
                name="Black Metal",
                description="Extreme metal style emphasizing atmosphere and intensity.",
                parent_genre=metal,
            ),
            MusicGenre(
                name="Doom Metal",
                description="Slow and heavy metal style focused on atmosphere and weight.",
                parent_genre=metal,
            ),
            MusicGenre(
                name="Nu Metal",
                description="1990s and 2000s metal fusion incorporating hip hop and alternative influences.",
                parent_genre=metal,
            ),
            MusicGenre(
                name="Power Metal",
                description="Melodic metal style emphasizing fantasy themes and dramatic compositions.",
                parent_genre=metal,
            ),
        ])

        # ------------------------------------------------------------
        # Pop
        # ------------------------------------------------------------

        pop = MusicGenre(
            name="Pop",
            description="Popular music focused on accessibility and broad audience appeal.",
        )

        music_genres.append(pop)

        music_genres.extend([
            MusicGenre(
                name="Teen Pop",
                description="Pop music targeted toward younger audiences.",
                parent_genre=pop,
            ),
            MusicGenre(
                name="Dance Pop",
                description="Pop music influenced by electronic dance production.",
                parent_genre=pop,
            ),
            MusicGenre(
                name="Synth Pop",
                description="Pop music centered around synthesizers and electronic production.",
                parent_genre=pop,
            ),
            MusicGenre(
                name="Bubblegum Pop",
                description="Highly accessible and upbeat pop music.",
                parent_genre=pop,
            ),
        ])

        # ------------------------------------------------------------
        # Hip Hop
        # ------------------------------------------------------------

        hip_hop = MusicGenre(
            name="Hip Hop",
            description="Music centered around rhythmic vocals, beats, and sampling.",
        )

        music_genres.append(hip_hop)

        music_genres.extend([
            MusicGenre(
                name="East Coast Hip Hop",
                description="Hip hop style associated with the eastern United States.",
                parent_genre=hip_hop,
            ),
            MusicGenre(
                name="West Coast Hip Hop",
                description="Hip hop style associated with the western United States.",
                parent_genre=hip_hop,
            ),
            MusicGenre(
                name="Gangsta Rap",
                description="Hip hop style focused on street narratives.",
                parent_genre=hip_hop,
            ),
            MusicGenre(
                name="Alternative Hip Hop",
                description="Experimental and unconventional hip hop.",
                parent_genre=hip_hop,
            ),
            MusicGenre(
                name="Trap",
                description="Modern hip hop style featuring electronic production.",
                parent_genre=hip_hop,
            ),
        ])

        # ------------------------------------------------------------
        # Electronic
        # ------------------------------------------------------------

        electronic = MusicGenre(
            name="Electronic",
            description="Music created primarily through electronic instruments and production.",
        )

        music_genres.append(electronic)

        music_genres.extend([
            MusicGenre(
                name="House",
                description="Electronic dance music style built around four-on-the-floor rhythms.",
                parent_genre=electronic,
            ),
            MusicGenre(
                name="Techno",
                description="Electronic genre emphasizing repetitive mechanical rhythms.",
                parent_genre=electronic,
            ),
            MusicGenre(
                name="Trance",
                description="Electronic style focused on melodic and atmospheric progression.",
                parent_genre=electronic,
            ),
            MusicGenre(
                name="Drum and Bass",
                description="Fast electronic genre centered around breakbeats and bass.",
                parent_genre=electronic,
            ),
            MusicGenre(
                name="Ambient",
                description="Atmospheric electronic music focused on texture.",
                parent_genre=electronic,
            ),
            MusicGenre(
                name="Synthwave",
                description="Electronic style inspired by 1980s music and media.",
                parent_genre=electronic,
            ),
        ])

        # ------------------------------------------------------------
        # Other Major Genres
        # ------------------------------------------------------------

        music_genres.extend([
            MusicGenre(
                name="Jazz",
                description="Music genre emphasizing improvisation and instrumentation.",
            ),
            MusicGenre(
                name="Classical",
                description="Traditional orchestral and composed music.",
            ),
            MusicGenre(
                name="Country",
                description="Music genre rooted in American folk traditions.",
            ),
            MusicGenre(
                name="Blues",
                description="Genre based around expressive vocals and twelve-bar structures.",
            ),
            MusicGenre(
                name="Folk",
                description="Traditional music based around cultural storytelling.",
            ),
            MusicGenre(
                name="Reggae",
                description="Jamaican music style emphasizing rhythm and bass.",
            ),
            MusicGenre(
                name="Latin",
                description="Music styles originating from Latin American traditions.",
            ),
            MusicGenre(
                name="World",
                description="Music from global cultural traditions.",
            ),
        ])

    # ------------------------------------------------------------------
    # Theme Population
    # ------------------------------------------------------------------

    def create_themes(self):
        """
        Create hierarchical media themes.
        """

        themes = []

        # --------------------------------------------------------------
        # Life Themes
        # --------------------------------------------------------------

        life = Theme(
            name="Life",
            description=(
                "Themes focused on personal experiences and human development."
            ),
        )

        themes.append(life)

        themes.extend([
            Theme(
                name="Coming of Age",
                description=(
                    "Stories centered around personal growth, maturity, and transition into adulthood."
                ),
                parent_theme=life,
            ),
            Theme(
                name="Slice of Life",
                description=(
                    "Stories focused on everyday experiences and ordinary moments."
                ),
                parent_theme=life,
            ),
        ])

        # --------------------------------------------------------------
        # Audience Themes
        # --------------------------------------------------------------

        audience = Theme(
            name="Audience",
            description="Themes related to intended viewer groups.",
        )

        themes.append(audience)

        themes.extend([
            Theme(
                name="Family",
                description="Programming suitable for family viewing.",
                parent_theme=audience,
            ),
            Theme(
                name="Children",
                description=(
                    "Programming designed primarily for younger audiences."
                ),
                parent_theme=audience,
            ),
        ])

        # --------------------------------------------------------------
        # Seasonal Themes
        # --------------------------------------------------------------

        seasonal = Theme(
            name="Seasonal",
            description="Themes associated with specific times of year.",
        )

        themes.append(seasonal)

        themes.extend([
            Theme(
                name="Holiday",
                description=(
                    "Programming associated with holidays and celebrations."
                ),
                parent_theme=seasonal,
            ),
            Theme(
                name="Summer",
                description=(
                    "Programming associated with summer seasons or vacations."
                ),
                parent_theme=seasonal,
            ),
        ])

        # --------------------------------------------------------------
        # Additional Themes
        # --------------------------------------------------------------

        themes.extend([
            Theme(
                name="Nostalgia",
                description=(
                    "Programming focused on memories, history, or retro culture."
                ),
            ),
            Theme(
                name="Educational",
                description="Programming designed to teach or inform.",
            ),
            Theme(
                name="Competition",
                description=(
                    "Programming centered around contests and challenges."
                ),
            ),
            Theme(
                name="Travel",
                description=(
                    "Programming focused on locations, cultures, and exploration."
                ),
            ),
        ])
