"""  
VISTOR MusicBrainz Authoritative Source  
  
Free, keyless lookup for music recordings via the MusicBrainz web service  
(https://musicbrainz.org/ws/2/). Enriches MusicVideo records that TMDB  
structurally cannot match. Returns the real first-release year and a  
controlled MusicGenre name derived from MusicBrainz genres/tags.  
  
The recording search/detail often reports a LATER release date (a re-issue /  
remaster / live recording) than when the song originally came out, because a  
YouTube title maps to whichever recording MusicBrainz scores highest, not the  
1996 studio original. To pin the TRUE original year we additionally search the  
RELEASE-GROUP endpoint:  
  
    release-group?query=artist:"Jamiroquai" AND releasegroup:"Virtual Insanity"  
  
and take the MINIMUM first-release-date across the returned release-groups.  
The original "Virtual Insanity" release-group is dated 1996, so this surfaces  
the true original year regardless of which recording the title maps to. The  
recording detail (release-groups) is kept as a secondary source, and the  
earliest non-zero of all of them wins.  
  
Genre is taken from the ARTIST's genres/tags FIRST, where styles like funk /  
acid jazz actually live. A specific recording or release is often tagged with  
a noisy one-off style (e.g. a compilation tagged "reggae"), so the artist is  
the more reliable source of the act's real style; the recording/detail tags  
are only a fallback when the artist carries none.  
  
MusicBrainz throttles to ~1 request/second and returns 503 when exceeded, so  
we space requests out and retry once. Every network failure is swallowed and  
degrades to whatever we already have (offline-safe: the smoke test never hits  
the network because `requests` is imported lazily).  
"""  
  
import re  
import time  
  
from core.logger import Logger  
  
_BASE = "https://musicbrainz.org/ws/2"  
_UA = "VISTOR/0.6 ( https://github.com/colinarosenthal/VISTOR )"  
_MIN_INTERVAL = 1.1  # seconds between requests (MusicBrainz asks for ~1/sec)  
  
# Strip common YouTube title noise before parsing artist/track.  
_TITLE_NOISE = re.compile(  
    r"\((official\s*(music\s*)?video|official\s*audio|lyric[s]?\s*video|"  
    r"audio|hd|4k|remaster(ed)?(\s*\d{4})?)\)",  
    re.IGNORECASE,  
)  
  
# MusicBrainz free-text genre/tag -> VISTOR controlled MusicGenre name.  
# Only names that exist in MetadataPopulation.create_music_genres() may appear  
# on the right; anything unmapped is dropped so we never invent a genre.  
_TAG_TO_MUSIC_GENRE = {  
    "rock": "Rock",  
    "pop": "Pop",  
    "hip hop": "Hip Hop",  
    "hip-hop": "Hip Hop",  
    "rap": "Hip Hop",  
    "electronic": "Electronic",  
    "dance": "Electronic",  
    "house": "Electronic",  
    "techno": "Electronic",  
    "jazz": "Jazz",  
    "funk": "Jazz",        # no Funk in the catalog; nearest controlled value  
    "acid jazz": "Jazz",  
    "soul": "Jazz",  
    "classical": "Classical",  
    "country": "Country",  
    "blues": "Blues",  
    "folk": "Folk",  
    "reggae": "Reggae",  
    "latin": "Latin",  
    "world": "World",  
    "r&b": "Pop",  
    "rhythm and blues": "Pop",  
    "metal": "Rock",  
    "punk": "Rock",  
    "indie": "Rock",  
    "alternative": "Rock",  
}  
  
  
class MusicBrainzSource:  
    """Best-effort music lookup. Never raises to the caller."""  
  
    def __init__(self, timeout=10):  
        self.timeout = timeout  
        self._last_request = 0.0  
  
    # Only used for MusicVideo; the composite router respects this hook.  
    def handles(self, media_type):  
        return media_type in (None, "", "MusicVideo")  
  
    # ------------------------------------------------------------------  
    # Public API  
    # ------------------------------------------------------------------  
    def lookup(self, title, year=None, media_type=None):  
        try:  
            import requests  # lazy: keeps the offline smoke test network-free  
        except ImportError:  
            Logger.warning("requests not installed; skipping MusicBrainz.")  
            return None  
  
        artist, track = self._split(title)  
        query = self._build_query(artist, track)  
        if not query:  
            return None  
  
        search = self._get(  
            requests,  
            f"{_BASE}/recording",  
            {"query": query, "fmt": "json", "limit": 5},  
        )  
        if not search:  
            return None  
  
        recordings = search.get("recordings") or []  
        if not recordings:  
            Logger.info(f"MusicBrainz: no recording match for '{title}'.")  
            return None  
  
        # Don't blindly take recordings[0]. Prefer a high-score match that  
        # already carries a first-release-date; that skips live/cover/  
        # compilation recordings whose date is empty and would yield year 0.  
        recording = self._pick_recording(recordings, artist)  
        mbid = recording.get("id")  
  
        # Year seed from the SEARCH result. This is often a re-issue year  
        # (e.g. 1999 for a 1996 song), so we treat it only as an upper bound  
        # and let the release-group search below pull it back to the original.  
        rec_year = self._year_from(recording.get("first-release-date"))  
  
        # GENRE: prefer the ARTIST's genres/tags FIRST. Styles like funk /  
        # acid jazz live on the artist; a specific recording/release is often  
        # tagged with a noisy one-off style (this is what produced the wrong  
        # "reggae" for Jamiroquai). Fall back to the recording's own tags only  
        # if the artist carries none.  
        music_genre = self._artist_genre(requests, recording)  
        if not music_genre:  
            music_genre = self._map_first(  
                (recording.get("genres") or []) + (recording.get("tags") or [])  
            )  
  
        # PRIMARY year source: the RELEASE-GROUP search. The original release  
        # group ("Virtual Insanity" / "Travelling Without Moving") is dated to  
        # the song's true debut year, independent of which recording the  
        # YouTube title mapped to. Take the EARLIEST across all returned  
        # release-groups.  
        rg_year = self._release_group_year(requests, artist, track)  
        rec_year = self._min_year(rec_year, rg_year)  
  
        # SECONDARY: detail-fetch the recording INCLUDING release-groups, in  
        # case the release-group search missed (odd punctuation, etc.). Also  
        # used to fill genre if neither the artist nor the search carried one.  
        if mbid:  
            detail = self._get(  
                requests,  
                f"{_BASE}/recording/{mbid}",  
                {"fmt": "json", "inc": "genres+tags+releases+release-groups"},  
            )  
            if detail:  
                detail_year = self._earliest_year(detail)  
                rec_year = self._min_year(rec_year, detail_year)  
                if not music_genre:  
                    music_genre = self._map_first(  
                        (detail.get("genres") or []) + (detail.get("tags") or [])  
                    )  
  
        Logger.info(  
            f"MusicBrainz matched '{title}' -> "  
            f"{rec_year or '?'} (genre={music_genre or '?'})."  
        )  
  
        return {  
            "release_year": rec_year,  
            "media_type": "MusicVideo",  
            "genres": ["Music"],       # broad controlled Genre stays "Music"  
            "music_genre": music_genre,  # specific style rides along  
        }  
  
    # ------------------------------------------------------------------  
    # Release-group search: the canonical "originally released" year  
    # ------------------------------------------------------------------  
    def _release_group_year(self, requests, artist, track):  
        """Search the release-group endpoint and return the EARLIEST  
        first-release-date year across all returned groups.  
  
        Query: artist:"<artist>" AND releasegroup:"<track>". The original  
        release-group for a song is dated to its debut year, so the minimum  
        across the results is the true original year regardless of which  
        recording (live/remaster/re-issue) the title maps to."""  
        if not track:  
            return 0  
  
        if artist:  
            query = f'artist:"{artist}" AND releasegroup:"{track}"'  
        else:  
            query = f'releasegroup:"{track}"'  
  
        data = self._get(  
            requests,  
            f"{_BASE}/release-group",  
            {"query": query, "fmt": "json", "limit": 25},  
        )  
        if not data:  
            return 0  
  
        artist_l = (artist or "").lower()  
        best = ""  
        for rg in data.get("release-groups") or []:  
            # If we know the artist, keep only groups credited to them so a  
            # same-named song by another artist can't drag the year.  
            if artist_l:  
                credited = False  
                for credit in rg.get("artist-credit") or []:  
                    name = ((credit or {}).get("artist") or {}).get("name", "")  
                    if artist_l in name.lower():  
                        credited = True  
                        break  
                if not credited:  
                    continue  
  
            date = rg.get("first-release-date") or ""  
            if date and (not best or date < best):  
                best = date  
  
        return self._year_from(best)  
  
    # ------------------------------------------------------------------  
    # HTTP with rate-limit spacing + one retry on 503  
    # ------------------------------------------------------------------  
    def _get(self, requests, url, params):  
        for attempt in range(2):  
            wait = _MIN_INTERVAL - (time.time() - self._last_request)  
            if wait > 0:  
                time.sleep(wait)  
            try:  
                resp = requests.get(  
                    url,  
                    params=params,  
                    headers={"User-Agent": _UA, "Accept": "application/json"},  
                    timeout=self.timeout,  
                )  
            except Exception as exc:  # noqa: BLE001 - never fail the caller  
                Logger.warning(f"MusicBrainz request failed: {exc!r}.")  
                return None  
            finally:  
                self._last_request = time.time()  
  
            if resp.status_code == 503 and attempt == 0:  
                Logger.warning("MusicBrainz 503 (rate limited); retrying once.")  
                time.sleep(_MIN_INTERVAL)  
                continue  
            if resp.status_code != 200:  
                Logger.warning(f"MusicBrainz HTTP {resp.status_code} for {url}.")  
                return None  
            try:  
                return resp.json()  
            except Exception as exc:  # noqa: BLE001  
                Logger.warning(f"MusicBrainz bad JSON: {exc!r}.")  
                return None  
        return None  
  
    def _artist_genre(self, requests, recording):  
        credits = recording.get("artist-credit") or []  
        if not credits:  
            return ""  
        artist = (credits[0] or {}).get("artist") or {}  
        mbid = artist.get("id")  
        if not mbid:  
            return ""  
        data = self._get(  
            requests,  
            f"{_BASE}/artist/{mbid}",  
            {"fmt": "json", "inc": "genres+tags"},  
        )  
        if not data:  
            return ""  
        return self._map_first(  
            (data.get("genres") or []) + (data.get("tags") or [])  
        )  
  
    # ------------------------------------------------------------------  
    # Helpers  
    # ------------------------------------------------------------------  
    def _pick_recording(self, recordings, artist):  
        """Choose the best candidate rather than blindly recordings[0].  
  
        Order of preference:  
          1. matches the parsed artist AND has a first-release-date  
          2. has a first-release-date (any artist)  
          3. matches the parsed artist  
          4. the top text-score hit (recordings[0])  
        Within each tier the earliest first-release-date wins, so the ORIGINAL  
        studio recording beats later live/compilation re-releases.  
        """  
        artist_l = (artist or "").lower()  
  
        def artist_matches(rec):  
            if not artist_l:  
                return False  
            for credit in rec.get("artist-credit") or []:  
                name = ((credit or {}).get("artist") or {}).get("name", "")  
                if artist_l in name.lower():  
                    return True  
            return False  
  
        def has_date(rec):  
            return bool(rec.get("first-release-date"))  
  
        def date_key(rec):  
            # Empty dates sort last so real dates are preferred.  
            return rec.get("first-release-date") or "9999"  
  
        for predicate in (  
            lambda r: artist_matches(r) and has_date(r),  
            has_date,  
            artist_matches,  
        ):  
            matches = [r for r in recordings if predicate(r)]  
            if matches:  
                return sorted(matches, key=date_key)[0]  
  
        return recordings[0]  
  
    @staticmethod  
    def _earliest_year(detail):  
        """Earliest year across the recording's first-release-date, every  
        release date, and every release-group first-release-date. The  
        release-group value is the canonical 'originally released' year."""  
        candidates = []  
  
        if detail.get("first-release-date"):  
            candidates.append(detail["first-release-date"])  
  
        for rel in detail.get("releases") or []:  
            if rel.get("date"):  
                candidates.append(rel["date"])  
            rg = rel.get("release-group") or {}  
            if rg.get("first-release-date"):  
                candidates.append(rg["first-release-date"])  
  
        best = ""  
        for date in candidates:  
            if date and (not best or date < best):  
                best = date  
        return MusicBrainzSource._year_from(best)  
  
    @staticmethod  
    def _min_year(a, b):  
        """Earliest non-zero year of the two, or 0 if both are empty."""  
        years = [y for y in (a, b) if y]  
        return min(years) if years else 0  
  
    @staticmethod  
    def _split(title):  
        """Parse 'Artist - Track (Official Video)' into (artist, track)."""  
        cleaned = _TITLE_NOISE.sub("", title or "")  
        cleaned = re.sub(r"\s{2,}", " ", cleaned).strip(" -")  
        if " - " in cleaned:  
            artist, track = cleaned.split(" - ", 1)  
            return artist.strip(), track.strip()  
        return "", cleaned  
  
    @staticmethod  
    def _build_query(artist, track):  
        if track and artist:  
            return f'recording:"{track}" AND artist:"{artist}"'  
        if track:  
            return f'recording:"{track}"'  
        return ""  
  
    @staticmethod  
    def _map_first(items):  
        """Highest-count genre/tag that maps to a controlled MusicGenre."""  
        for item in sorted(  
            items or [], key=lambda t: t.get("count", 0), reverse=True  
        ):  
            mapped = _TAG_TO_MUSIC_GENRE.get((item.get("name") or "").lower())  
            if mapped:  
                return mapped  
        return ""  
  
    @staticmethod  
    def _year_from(date):  
        if date and len(date) >= 4 and date[:4].isdigit():  
            return int(date[:4])  
        return 0