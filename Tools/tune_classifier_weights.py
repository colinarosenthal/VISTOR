"""
VISTOR Classifier Weight Tuner

Optimizes the per-signal weights used by MediaClassifier.classify_type against
a labeled sample set, then writes the best weights to
Metadata/data/classifier_weights.json (which the classifier loads on init).

Usage (from repo root, with src/ on PYTHONPATH like the other tools):
    python tools/tune_classifier_weights.py

Deterministic, offline, no third-party deps: it just re-instantiates the
classifier with candidate weights and counts correct labels.
"""

import json
import sys
from pathlib import Path

# Match how add_media_web.py bootstraps sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from metadata.services.media_classifier import (  # noqa: E402
    MediaClassifier,
    _DEFAULT_WEIGHTS,   # rename to your actual default-weights constant
)

_SAMPLES = Path("Metadata/data/classifier_samples.json")
_OUT = Path("Metadata/data/classifier_weights.json")

# Candidate multipliers tried per weight during coordinate ascent.
_GRID = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]


def _accuracy(weights, samples):
    _OUT.parent.mkdir(parents=True, exist_ok=True)
    _OUT.write_text(json.dumps(weights), encoding="utf-8")
    clf = MediaClassifier()  # re-reads classifier_weights.json on init
    correct = 0
    for s in samples:
        if clf.classify_type(s.get("scraped") or {}) == s.get("label"):
            correct += 1
    return correct / len(samples) if samples else 0.0


def main():
    samples = json.loads(_SAMPLES.read_text(encoding="utf-8"))
    weights = dict(_DEFAULT_WEIGHTS)

    best = _accuracy(weights, samples)
    print(f"baseline accuracy: {best:.3f}")

    improved = True
    while improved:  # coordinate ascent until no single tweak helps
        improved = False
        for key, base in list(weights.items()):
            for mult in _GRID:
                trial = dict(weights)
                trial[key] = round(base * mult, 4)
                acc = _accuracy(trial, samples)
                if acc > best:
                    best, weights, improved = acc, trial, True

    _OUT.write_text(json.dumps(weights, indent=2), encoding="utf-8")
    print(f"tuned accuracy: {best:.3f} -> wrote {_OUT}")


if __name__ == "__main__":
    main()
