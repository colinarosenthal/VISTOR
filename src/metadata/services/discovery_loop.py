"""  
VISTOR Discovery Loop  
  
Autonomous catalogue expansion. Uses a catalogued MediaItem (or channel  
spec) as a seed, asks RecommendationSource for similar titles, then acts  
according to Config.recommendation_mode:  
  
    suggest_only : return suggestions; write/download nothing (default).  
    assisted     : find candidate source URLs; still return for confirm.  
    automatic    : build + ingest + download with no interaction, capped  
                   by max_auto_additions_per_week.  
  
Gated entirely on Config.recommended_media, so it is OFF by default.  
Offline-safe: with no TMDB key RecommendationSource returns [] and this  
loop is a no-op.  
"""  
  
from core.config import Config  
from core.logger import Logger  
from metadata.services.record_builder import RecordBuilder  
from metadata.services.media_ingestor import MediaIngestor  
from metadata.services.enrichment.recommendation_source import RecommendationSource  
  
  
class DiscoveryLoop:  
    def __init__(self, metadata_path="Metadata/data", config=None):  
        self.config = config or Config().load()  
        self.recommender = RecommendationSource()  
        self.builder = RecordBuilder()  
        self.ingestor = MediaIngestor(metadata_path)  
  
    def run_from_seed(self, tmdb_id, media_type="Movie", limit=8):  
        """Expand the catalogue from one seed TMDB id. Returns a report."""  
        report = {"suggested": [], "committed": [], "skipped_cap": []}  
  
        if not getattr(self.config, "recommended_media", False):  
            Logger.info("Recommended media disabled; discovery loop is a no-op.")  
            return report  
  
        mode = getattr(self.config, "recommendation_mode", "suggest_only")  
        suggestions = self.recommender.recommend(tmdb_id, media_type, limit=limit)  
        report["suggested"] = suggestions  
  
        if mode == "suggest_only":  
            Logger.info(f"suggest_only: {len(suggestions)} suggestion(s), none acquired.")  
            return report  
  
        # assisted + automatic both need a candidate source URL per suggestion.  
        remaining = getattr(self.config, "max_auto_additions_per_week", 0)  
  
        for cand in suggestions:  
            url = self._discover_source_url(cand)      # TODO: real archive search  
            if not url:  
                continue  
            cand["source_url"] = url  
  
            if mode == "assisted":  
                # Surface for human confirm (same confirm step as the web UI).  
                continue  
  
            # automatic  
            if remaining <= 0:  
                report["skipped_cap"].append(cand.get("tmdb_id"))  
                continue  
            record = self.builder.build(url, overrides={"type": cand["media_type"]})  
            result = self.ingestor.ingest_records([record], download=True)  
            report["committed"].append(cand.get("tmdb_id"))  
            remaining -= 1  
  
        Logger.info(  
            f"Discovery ({mode}): suggested={len(report['suggested'])} "  
            f"committed={len(report['committed'])} capped={len(report['skipped_cap'])}."  
        )  
        return report  
  
    def _discover_source_url(self, candidate):  
        """Search public archives for a playable URL for a suggested title.  
        Placeholder until a real Internet Archive / YouTube search backend  
        lands — returns None so 'automatic' mode stays inert until wired."""  
        return None