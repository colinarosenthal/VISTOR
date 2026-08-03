"""  
VISTOR Media Classifier  
  
Deterministic, offline best-guess classification of a scraped info-dict  
(as returned by MediaDescriber / yt-dlp) into:  
  
    - a VISTOR media type string the loader understands  
      ("Movie", "MusicVideo", "Commercial", "Episode")  
    - a list of genre names drawn ONLY from the controlled Genre  
      vocabulary in MetadataPopulation.create_genres()  
  
No network, no heavy deps. Guesses are logged so the user knows to verify.  
Precedence in RecordBuilder is: overrides > authoritative > classified >  
scraped > default, so this only fills gaps the caller did not specify.  
"""  
  
from core.logger import Logger  
  
  
# The controlled Genre vocabulary (must match  
# MetadataPopulation.create_genres()). Only these names may be emitted.  
_CONTROLLED_GENRES = {  
    "Action",  
    "Adventure",  
    "Animation",  
    "Comedy",  
    "Drama",  
    "Documentary",  
    "Horror",  
    "Science Fiction",  
    "Fantasy",  
    "Reality",  
    "Sports",  
    "News",  
    "Music",  
}  
  
# YouTube "categories" -> controlled Genre names.  
_CATEGORY_TO_GENRES = {  
    "music": ["Music"],  
    "film & animation": ["Animation"],  
    "sports": ["Sports"],  
    "news & politics": ["News"],  
    "comedy": ["Comedy"],  
    "entertainment": [],  
    "gaming": [],  
    "howto & style": ["Documentary"],  
    "education": ["Documentary"],  
    "science & technology": ["Documentary", "Science Fiction"],  
    "people & blogs": [],  
    "travel & events": ["Adventure"],  
}  
  
# Free-text keyword hints (matched against title + tags, lowercased).  
_KEYWORD_TO_GENRES = {  
    "horror": "Horror",  
    "sci-fi": "Science Fiction",  
    "science fiction": "Science Fiction",  
    "fantasy": "Fantasy",  
    "documentary": "Documentary",  
    "comedy": "Comedy",  
    "action": "Action",  
    "adventure": "Adventure",  
    "drama": "Drama",  
    "anime": "Animation",  
    "animated": "Animation",  
    "cartoon": "Animation",  
    "reality": "Reality",  
    "concert": "Music",  
    "music video": "Music",  
    "official video": "Music",  
    "news": "News",  
    "sports": "Sports",  
}  
  
# A YouTube "Music" video longer than this is more likely a concert/film  
# than a single music video; below it, treat as a music video.  
_MUSIC_VIDEO_MAX_SECONDS = 15 * 60  
  
# Anything at least this long is treated as a Movie rather than an Episode.  
_MOVIE_MIN_SECONDS = 70 * 60  
  
  
class MediaClassifier:  
    """Best-guess (type, genres) from a scraped info-dict. Never raises."""  
  
    def classify_type(self, scraped):  
        """  
        Return a loader media-type string or None if undecidable.  
  
        `scraped` is a dict shaped like a yt-dlp info-dict. Missing keys  
        are tolerated; an empty/None dict yields None.  
        """  
  
        scraped = scraped or {}  
  
        categories = [c.lower() for c in (scraped.get("categories") or [])]  
        duration = scraped.get("duration") or 0  
        text = self._searchable_text(scraped)  
  
        is_music_category = "music" in categories  
        has_music_title = any(  
            k in text  
            for k in ("official video", "official music video", "music video")  
        )  
  
        # Music video: YouTube category=Music OR a music-video title keyword.  
        # Short -> MusicVideo; feature-length -> concert film held as a Movie.  
        if is_music_category or has_music_title:  
            if not duration or duration <= _MUSIC_VIDEO_MAX_SECONDS:  
                reason = (  
                    "YouTube category=Music"  
                    if is_music_category  
                    else "music-video title keyword"  
                )  
                return self._log_guess("MusicVideo", reason)  
            return self._log_guess("Movie", "long-form music content")  
  
        # Long-form film & animation -> Movie.  
        if "film & animation" in categories:  
            if not duration or duration >= _MOVIE_MIN_SECONDS:  
                return self._log_guess("Movie", "YouTube category=Film & Animation")  
  
        # Duration fallback: feature-length -> Movie.  
        if duration and duration >= _MOVIE_MIN_SECONDS:  
            return self._log_guess("Movie", "duration >= 70min")  
  
        # Undecidable: let RecordBuilder fall back to its default/override.  
        return None 
  
    def classify_genres(self, scraped):  
        """  
        Return a de-duplicated list of controlled Genre names, possibly  
        empty. Never emits a name outside _CONTROLLED_GENRES.  
        """  
  
        scraped = scraped or {}  
  
        found = []  
  
        # 1. Map YouTube categories.  
        for category in (scraped.get("categories") or []):  
            for name in _CATEGORY_TO_GENRES.get(category.lower(), []):  
                found.append(name)  
  
        # 2. Keyword hints from title + tags.  
        text = self._searchable_text(scraped)  
        for keyword, name in _KEYWORD_TO_GENRES.items():  
            if keyword in text:  
                found.append(name)  
  
        # 3. Keep only controlled-vocabulary names, de-duplicated, ordered.  
        result = []  
        for name in found:  
            if name in _CONTROLLED_GENRES and name not in result:  
                result.append(name)  
  
        if result:  
            Logger.info(f"Classified genres (verify): {result}")  
  
        return result  
  
    # ------------------------------------------------------------------  
    # Helpers  
    # ------------------------------------------------------------------  
  
    def _searchable_text(self, scraped):  
        """Lowercased title + tags joined for keyword scanning."""  
  
        parts = [scraped.get("title") or ""]  
        parts.extend(scraped.get("tags") or [])  
        return " ".join(parts).lower()  
  
    def _log_guess(self, media_type, reason):  
        Logger.info(f"Classified type '{media_type}' ({reason}); verify if wrong.")  
        return media_type