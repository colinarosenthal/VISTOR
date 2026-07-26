"""
VISTOR Metadata Population Service

Creates default metadata objects used by VISTOR.
"""

from metadata.vocabulary.genre import Genre  
from metadata.vocabulary.music_genre import MusicGenre  
from metadata.vocabulary.theme import Theme  
from metadata.vocabulary.content_rating import ContentRating  
from metadata.vocabulary.country import Country  
from metadata.vocabulary.language import Language  
from metadata.vocabulary.tag import Tag
from metadata.library.network import Network

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

        return music_genres

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
        return themes

    # ------------------------------------------------------------------  
    # Content Rating Population  
    # ------------------------------------------------------------------  
  
    def create_content_ratings(self):  
        """  
        Create default VISTOR content ratings.  
        """  
  
        return [  
  
            # ----------------------------------------------------------  
            # Unrated  
            # ----------------------------------------------------------  
  
            ContentRating(  
                name="Unrated",  
                system="",  
                country="",  
                min_age=0,  
                description="No official rating has been assigned.",  
            ),  
            ContentRating(  
                name="Unknown",  
                system="",  
                country="",  
                min_age=0,  
                description="The rating is unknown or unavailable.",  
            ),  
  
            # ----------------------------------------------------------  
            # Motion Picture Association (United States)  
            # ----------------------------------------------------------  
  
            ContentRating(  
                name="G",  
                system="MPAA",  
                country="United States",  
                min_age=0,  
                description="General audiences; all ages admitted.",  
            ),  
            ContentRating(  
                name="PG",  
                system="MPAA",  
                country="United States",  
                min_age=0,  
                description=(  
                    "Parental guidance suggested; some material may not be "  
                    "suitable for children."  
                ),  
            ),  
            ContentRating(  
                name="PG-13",  
                system="MPAA",  
                country="United States",  
                min_age=13,  
                description=(  
                    "Parents strongly cautioned; some material may be "  
                    "inappropriate for children under 13."  
                ),  
            ),  
            ContentRating(  
                name="R",  
                system="MPAA",  
                country="United States",  
                min_age=17,  
                description=(  
                    "Restricted; under 17 requires an accompanying parent "  
                    "or adult guardian."  
                ),  
            ),  
            ContentRating(  
                name="NC-17",  
                system="MPAA",  
                country="United States",  
                min_age=18,  
                description="No one 17 and under admitted.",  
            ),  
  
            # ----------------------------------------------------------  
            # Television Parental Guidelines (United States)  
            # ----------------------------------------------------------  
  
            ContentRating(  
                name="TV-Y",  
                system="TV Parental Guidelines",  
                country="United States",  
                min_age=0,  
                description="Designed to be appropriate for all children.",  
            ),  
            ContentRating(  
                name="TV-Y7",  
                system="TV Parental Guidelines",  
                country="United States",  
                min_age=7,  
                description="Directed to children age 7 and older.",  
            ),  
            ContentRating(  
                name="TV-G",  
                system="TV Parental Guidelines",  
                country="United States",  
                min_age=0,  
                description="Suitable for all ages.",  
            ),  
            ContentRating(  
                name="TV-PG",  
                system="TV Parental Guidelines",  
                country="United States",  
                min_age=0,  
                description="Parental guidance suggested.",  
            ),  
            ContentRating(  
                name="TV-14",  
                system="TV Parental Guidelines",  
                country="United States",  
                min_age=14,  
                description=(  
                    "Parents strongly cautioned; may be unsuitable for "  
                    "children under 14."  
                ),  
            ),  
            ContentRating(  
                name="TV-MA",  
                system="TV Parental Guidelines",  
                country="United States",  
                min_age=17,  
                description=(  
                    "Intended for mature audiences; may be unsuitable for "  
                    "children under 17."  
                ),  
            ),  
  
            # ----------------------------------------------------------  
            # British Board of Film Classification (United Kingdom)  
            # ----------------------------------------------------------  
  
            ContentRating(  
                name="U",  
                system="BBFC",  
                country="United Kingdom",  
                min_age=0,  
                description="Universal; suitable for all.",  
            ),  
            ContentRating(  
                name="PG",  
                system="BBFC",  
                country="United Kingdom",  
                min_age=0,  
                description=(  
                    "Parental guidance; general viewing, but some scenes "  
                    "may be unsuitable for young children."  
                ),  
            ),  
            ContentRating(  
                name="12",  
                system="BBFC",  
                country="United Kingdom",  
                min_age=12,  
                description="Suitable for 12 years and over.",  
            ),  
            ContentRating(  
                name="12A",  
                system="BBFC",  
                country="United Kingdom",  
                min_age=12,  
                description=(  
                    "Cinema release suitable for 12 years and over; under "  
                    "12 admitted with an adult."  
                ),  
            ),  
            ContentRating(  
                name="15",  
                system="BBFC",  
                country="United Kingdom",  
                min_age=15,  
                description="Suitable only for 15 years and over.",  
            ),  
            ContentRating(  
                name="18",  
                system="BBFC",  
                country="United Kingdom",  
                min_age=18,  
                description="Suitable only for adults.",  
            ),  
        ]

    # ------------------------------------------------------------------  
    # Country Population  
    # ------------------------------------------------------------------  
  
    def create_countries(self):  
        """  
        Create default VISTOR countries.  
        """  
  
        return [  
  
            # ----------------------------------------------------------  
            # North America  
            # ----------------------------------------------------------  
  
            Country(  
                name="United States",  
                iso_alpha2="US",  
                iso_alpha3="USA",  
                region="North America",  
            ),  
            Country(  
                name="Canada",  
                iso_alpha2="CA",  
                iso_alpha3="CAN",  
                region="North America",  
            ),  
            Country(  
                name="Mexico",  
                iso_alpha2="MX",  
                iso_alpha3="MEX",  
                region="North America",  
            ),  
  
            # ----------------------------------------------------------  
            # South America  
            # ----------------------------------------------------------  
  
            Country(  
                name="Brazil",  
                iso_alpha2="BR",  
                iso_alpha3="BRA",  
                region="South America",  
            ),  
            Country(  
                name="Argentina",  
                iso_alpha2="AR",  
                iso_alpha3="ARG",  
                region="South America",  
            ),  
  
            # ----------------------------------------------------------  
            # Europe  
            # ----------------------------------------------------------  
  
            Country(  
                name="United Kingdom",  
                iso_alpha2="GB",  
                iso_alpha3="GBR",  
                region="Europe",  
            ),  
            Country(  
                name="Ireland",  
                iso_alpha2="IE",  
                iso_alpha3="IRL",  
                region="Europe",  
            ),  
            Country(  
                name="France",  
                iso_alpha2="FR",  
                iso_alpha3="FRA",  
                region="Europe",  
            ),  
            Country(  
                name="Germany",  
                iso_alpha2="DE",  
                iso_alpha3="DEU",  
                region="Europe",  
            ),  
            Country(  
                name="Spain",  
                iso_alpha2="ES",  
                iso_alpha3="ESP",  
                region="Europe",  
            ),  
            Country(  
                name="Italy",  
                iso_alpha2="IT",  
                iso_alpha3="ITA",  
                region="Europe",  
            ),  
            Country(  
                name="Netherlands",  
                iso_alpha2="NL",  
                iso_alpha3="NLD",  
                region="Europe",  
            ),  
            Country(  
                name="Sweden",  
                iso_alpha2="SE",  
                iso_alpha3="SWE",  
                region="Europe",  
            ),  
            Country(  
                name="Russia",  
                iso_alpha2="RU",  
                iso_alpha3="RUS",  
                region="Europe",  
            ),  
  
            # ----------------------------------------------------------  
            # Asia  
            # ----------------------------------------------------------  
  
            Country(  
                name="Japan",  
                iso_alpha2="JP",  
                iso_alpha3="JPN",  
                region="Asia",  
            ),  
            Country(  
                name="South Korea",  
                iso_alpha2="KR",  
                iso_alpha3="KOR",  
                region="Asia",  
            ),  
            Country(  
                name="China",  
                iso_alpha2="CN",  
                iso_alpha3="CHN",  
                region="Asia",  
            ),  
            Country(  
                name="India",  
                iso_alpha2="IN",  
                iso_alpha3="IND",  
                region="Asia",  
            ),  
            Country(  
                name="Hong Kong",  
                iso_alpha2="HK",  
                iso_alpha3="HKG",  
                region="Asia",  
            ),  
  
            # ----------------------------------------------------------  
            # Oceania  
            # ----------------------------------------------------------  
  
            Country(  
                name="Australia",  
                iso_alpha2="AU",  
                iso_alpha3="AUS",  
                region="Oceania",  
            ),  
            Country(  
                name="New Zealand",  
                iso_alpha2="NZ",  
                iso_alpha3="NZL",  
                region="Oceania",  
            ),  
  
            # ----------------------------------------------------------  
            # Africa  
            # ----------------------------------------------------------  
  
            Country(  
                name="South Africa",  
                iso_alpha2="ZA",  
                iso_alpha3="ZAF",  
                region="Africa",  
            ),  
            Country(  
                name="Nigeria",  
                iso_alpha2="NG",  
                iso_alpha3="NGA",  
                region="Africa",  
            ),  
        ]

    # ------------------------------------------------------------------  
    # Language Population  
    # ------------------------------------------------------------------  
  
    def create_languages(self):  
        """  
        Create default VISTOR languages.  
        """  
  
        return [  
  
            # ----------------------------------------------------------  
            # Widely Spoken  
            # ----------------------------------------------------------  
  
            Language(  
                name="English",  
                iso_639_1="en",  
                iso_639_2="eng",  
                native_name="English",  
            ),  
            Language(  
                name="Spanish",  
                iso_639_1="es",  
                iso_639_2="spa",  
                native_name="Español",  
            ),  
            Language(  
                name="Mandarin Chinese",  
                iso_639_1="zh",  
                iso_639_2="zho",  
                native_name="中文",  
            ),  
            Language(  
                name="Hindi",  
                iso_639_1="hi",  
                iso_639_2="hin",  
                native_name="हिन्दी",  
            ),  
            Language(  
                name="Arabic",  
                iso_639_1="ar",  
                iso_639_2="ara",  
                native_name="العربية",  
            ),  
            Language(  
                name="Portuguese",  
                iso_639_1="pt",  
                iso_639_2="por",  
                native_name="Português",  
            ),  
            Language(  
                name="Russian",  
                iso_639_1="ru",  
                iso_639_2="rus",  
                native_name="Русский",  
            ),  
  
            # ----------------------------------------------------------  
            # European  
            # ----------------------------------------------------------  
  
            Language(  
                name="French",  
                iso_639_1="fr",  
                iso_639_2="fra",  
                native_name="Français",  
            ),  
            Language(  
                name="German",  
                iso_639_1="de",  
                iso_639_2="deu",  
                native_name="Deutsch",  
            ),  
            Language(  
                name="Italian",  
                iso_639_1="it",  
                iso_639_2="ita",  
                native_name="Italiano",  
            ),  
            Language(  
                name="Dutch",  
                iso_639_1="nl",  
                iso_639_2="nld",  
                native_name="Nederlands",  
            ),  
            Language(  
                name="Swedish",  
                iso_639_1="sv",  
                iso_639_2="swe",  
                native_name="Svenska",  
            ),  
            Language(  
                name="Polish",  
                iso_639_1="pl",  
                iso_639_2="pol",  
                native_name="Polski",  
            ),  
            Language(  
                name="Greek",  
                iso_639_1="el",  
                iso_639_2="ell",  
                native_name="Ελληνικά",  
            ),  
  
            # ----------------------------------------------------------  
            # Asian  
            # ----------------------------------------------------------  
  
            Language(  
                name="Japanese",  
                iso_639_1="ja",  
                iso_639_2="jpn",  
                native_name="日本語",  
            ),  
            Language(  
                name="Korean",  
                iso_639_1="ko",  
                iso_639_2="kor",  
                native_name="한국어",  
            ),  
            Language(  
                name="Thai",  
                iso_639_1="th",  
                iso_639_2="tha",  
                native_name="ไทย",  
            ),  
            Language(  
                name="Vietnamese",  
                iso_639_1="vi",  
                iso_639_2="vie",  
                native_name="Tiếng Việt",  
            ),  
            Language(  
                name="Turkish",  
                iso_639_1="tr",  
                iso_639_2="tur",  
                native_name="Türkçe",  
            ),  
            Language(  
                name="Hebrew",  
                iso_639_1="he",  
                iso_639_2="heb",  
                native_name="עברית",  
            ),  
  
            # ----------------------------------------------------------  
            # Other  
            # ----------------------------------------------------------  
  
            Language(  
                name="Latin",  
                iso_639_1="la",  
                iso_639_2="lat",  
                native_name="Latina",  
            ),  
            Language(  
                name="Silent",  
                iso_639_1="",  
                iso_639_2="zxx",  
                native_name="No linguistic content",  
            ),  
        ]
# ------------------------------------------------------------------  
    # Tag Population  
    # ------------------------------------------------------------------  
  
    def create_tags(self):  
        """  
        Create default VISTOR tags.  
        """  
  
        return [  
  
            # ----------------------------------------------------------  
            # Format  
            # ----------------------------------------------------------  
  
            Tag(  
                name="Black and White",  
                description="Content presented without color.",  
                category="Format",  
            ),  
            Tag(  
                name="Widescreen",  
                description="Content presented in a widescreen aspect ratio.",  
                category="Format",  
            ),  
            Tag(  
                name="Remastered",  
                description="Content that has been restored or remastered.",  
                category="Format",  
            ),  
            Tag(  
                name="Live",  
                description="Content broadcast or recorded live.",  
                category="Format",  
            ),  
  
            # ----------------------------------------------------------  
            # Tone  
            # ----------------------------------------------------------  
  
            Tag(  
                name="Dark",  
                description="Content with a serious or grim tone.",  
                category="Tone",  
            ),  
            Tag(  
                name="Lighthearted",  
                description="Content with a cheerful or easygoing tone.",  
                category="Tone",  
            ),  
            Tag(  
                name="Suspenseful",  
                description="Content that builds tension and anticipation.",  
                category="Tone",  
            ),  
            Tag(  
                name="Feel Good",  
                description="Content intended to leave a positive impression.",  
                category="Tone",  
            ),  
  
            # ----------------------------------------------------------  
            # Audience  
            # ----------------------------------------------------------  
  
            Tag(  
                name="Cult Classic",  
                description="Content with a dedicated niche following.",  
                category="Audience",  
            ),  
            Tag(  
                name="Award Winning",  
                description="Content that has received notable awards.",  
                category="Audience",  
            ),  
            Tag(  
                name="Based on True Events",  
                description="Content inspired by real people or events.",  
                category="Audience",  
            ),  
            Tag(  
                name="Based on a Book",  
                description="Content adapted from a written work.",  
                category="Audience",  
            ),  
  
            # ----------------------------------------------------------  
            # Production  
            # ----------------------------------------------------------  
  
            Tag(  
                name="Independent",  
                description="Content produced outside major studios.",  
                category="Production",  
            ),  
            Tag(  
                name="Foreign",  
                description="Content produced outside the primary market.",  
                category="Production",  
            ),  
            Tag(  
                name="Miniseries",  
                description="A short-form series with a limited number of episodes.",  
                category="Production",  
            ),  
        ]

    # ------------------------------------------------------------------  
    # Network Population  
    # ------------------------------------------------------------------  
  
    def create_networks(self):  
        """  
        Create default VISTOR networks.  
        """  
  
        return [  
  
            # ----------------------------------------------------------  
            # Broadcast (United States)  
            # ----------------------------------------------------------  
  
            Network(  
                id="abc",  
                name="American Broadcasting Company",  
                abbreviation="ABC",  
                description="American broadcast television network.",  
            ),  
            Network(  
                id="cbs",  
                name="Columbia Broadcasting System",  
                abbreviation="CBS",  
                description="American broadcast television network.",  
            ),  
            Network(  
                id="nbc",  
                name="National Broadcasting Company",  
                abbreviation="NBC",  
                description="American broadcast television network.",  
            ),  
            Network(  
                id="fox",  
                name="Fox Broadcasting Company",  
                abbreviation="FOX",  
                description="American broadcast television network.",  
            ),  
            Network(  
                id="pbs",  
                name="Public Broadcasting Service",  
                abbreviation="PBS",  
                description="American public broadcast television network.",  
            ),  
  
            # ----------------------------------------------------------  
            # Cable (United States)  
            # ----------------------------------------------------------  
  
            Network(  
                id="hbo",  
                name="Home Box Office",  
                abbreviation="HBO",  
                description="American premium cable network.",  
            ),  
            Network(  
                id="amc",  
                name="American Movie Classics",  
                abbreviation="AMC",  
                description="American basic cable network.",  
            ),  
            Network(  
                id="cnn",  
                name="Cable News Network",  
                abbreviation="CNN",  
                description="American cable news network.",  
            ),  
            Network(  
                id="espn",  
                name="Entertainment and Sports Programming Network",  
                abbreviation="ESPN",  
                description="American cable sports network.",  
            ),  
            Network(  
                id="mtv",  
                name="Music Television",  
                abbreviation="MTV",  
                description="American cable music and entertainment network.",  
            ),  
            Network(  
                id="nickelodeon",  
                name="Nickelodeon",  
                abbreviation="NICK",  
                description="American children's cable network.",  
            ),  
            Network(  
                id="cartoon_network",  
                name="Cartoon Network",  
                abbreviation="CN",  
                description="American animation cable network.",  
            ),  
            Network(  
                id="disney_channel",  
                name="Disney Channel",  
                abbreviation="DISN",  
                description="American children's cable network.",  
            ),  
  
            # ----------------------------------------------------------  
            # International  
            # ----------------------------------------------------------  
  
            Network(  
                id="bbc",  
                name="British Broadcasting Corporation",  
                abbreviation="BBC",  
                description="British public broadcast network.",  
            ),  
        ]