"""
Seed VISTOR controlled-vocabulary files from MetadataPopulation.

Regenerates the seven vocab JSONs the loader relinks names against.
Writes ONLY vocab files -- never media.json -- so it is safe to re-run.

Run from the project root:  python scripts/seed_vocabulary.py
"""

import json
import sys
from pathlib import Path

# Make `src` importable when run from the project root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from metadata.services.metadata_population import MetadataPopulation

OUT = Path("Metadata/data")
OUT.mkdir(parents=True, exist_ok=True)

pop = MetadataPopulation()


def write(name, data):
    with open(OUT / name, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def flat(obj):
    """Mirror MetadataSerializer._object_to_dictionary (public attrs only)."""
    return {k: v for k, v in vars(obj).items() if not k.startswith("_")}


# --- Flat vocabularies (primitive attributes only) -------------------
write("genres.json", [flat(g) for g in pop.create_genres()])
write("tags.json", [flat(t) for t in pop.create_tags()])
write("languages.json", [flat(l) for l in pop.create_languages()])
write("countries.json", [flat(c) for c in pop.create_countries()])
write("content_ratings.json", [flat(r) for r in pop.create_content_ratings()])

# --- Parented vocabularies (reference resolved to a name) ------------
write("music_genres.json", [
    {
        "name": g.get_name(),
        "description": g.get_description(),
        "parent_genre": (
            g.get_parent_genre().get_name() if g.get_parent_genre() else None
        ),
    }
    for g in pop.create_music_genres()
])

write("themes.json", [
    {
        "name": t.get_name(),
        "description": t.get_description(),
        "parent_theme": (
            t.get_parent_theme().get_name() if t.get_parent_theme() else None
        ),
    }
    for t in pop.create_themes()
])

print("Vocabulary seeded:", ", ".join(sorted(p.name for p in OUT.glob("*.json"))))
