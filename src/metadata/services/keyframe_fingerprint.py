"""
VISTOR Keyframe Fingerprinting

Generates and compares perceptual "keyframe" fingerprints for media assets.

A fingerprint is a short, fixed-length hex string identifying the *visual
content* of a file independently of its filename or container. Fingerprints
persist on MediaAsset even after the file is evicted, so when a source
disappears the resolver can search other archives for a file whose
fingerprint matches -- or a close-enough substitute.

Extraction is pluggable. StubKeyframeExtractor is fully deterministic and
dependency-free (derives a fingerprint from stable asset attributes) so the
headless build and tests never need real media or a video decoder. Once
media is gathered automatically, inject a real extractor (ffmpeg/OpenCV
keyframe hashing) implementing the same extract() signature -- nothing else
in the pipeline changes.
"""

import hashlib

from core.logger import Logger


# Fixed hex length so fingerprints are always comparable.
FINGERPRINT_LENGTH = 32


class KeyframeExtractor:
    """Interface for anything that produces a fingerprint for an asset."""

    def extract(self, asset):
        """Return a fixed-length hex fingerprint string for the asset."""

        raise NotImplementedError


class StubKeyframeExtractor(KeyframeExtractor):
    """
    Zero-dependency deterministic fingerprint.

    Derives a stable hex fingerprint from the asset's identifying/technical
    attributes rather than decoding pixels. Two assets with the same visual
    identity (same checksum/runtime/resolution/filename) fingerprint
    identically; a real perceptual extractor later replaces this class.
    """

    def extract(self, asset):
        seed = "|".join(
            str(part)
            for part in (
                asset.get_checksum(),
                asset.get_runtime_seconds(),
                asset.get_resolution()[0],
                asset.get_resolution()[1],
                asset.get_filename(),
            )
        )

        digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()

        return digest[:FINGERPRINT_LENGTH]


class KeyframeFingerprintService:
    """Assigns and compares keyframe fingerprints across media assets."""

    def __init__(self, extractor: KeyframeExtractor = None):
        # Dependency injection: default to the zero-dep stub, swap in a real
        # ffmpeg/OpenCV extractor later without touching callers.
        self.extractor = extractor or StubKeyframeExtractor()

    # --------------------------------------------------------------
    # Generation
    # --------------------------------------------------------------

    def generate(self, asset):
        """Compute and store a fingerprint on the asset. Returns it."""

        fingerprint = self.extractor.extract(asset)
        asset.set_fingerprint(fingerprint)

        Logger.info(
            f"Fingerprinted asset '{asset.get_asset_id()}' -> {fingerprint}."
        )

        return fingerprint

    def ensure_fingerprint(self, asset):
        """Fingerprint the asset only if it doesn't already have one."""

        if asset.get_fingerprint():
            return asset.get_fingerprint()

        return self.generate(asset)

    # --------------------------------------------------------------
    # Comparison
    # --------------------------------------------------------------

    def distance(self, first: str, second: str):
        """
        Return a 0.0-1.0 dissimilarity between two fingerprints.

        0.0 == identical, 1.0 == completely different. Per-character Hamming
        distance over the fixed-length hex strings; any length difference
        counts as additional mismatches.
        """

        if not first or not second:
            return 1.0

        mismatches = sum(1 for a, b in zip(first, second) if a != b)
        mismatches += abs(len(first) - len(second))

        return mismatches / max(len(first), len(second))

    def find_match(self, fingerprint, candidates, threshold=0.25):
        """
        Return (asset, distance) whose fingerprint is closest to
        `fingerprint` and within `threshold`, or None.

        Used to locate a replacement when the original source is gone: search
        other archives' assets for one whose fingerprint matches the missing
        file (or a close substitute).
        """

        best = None
        best_distance = threshold

        for candidate in candidates:
            candidate_fp = candidate.get_fingerprint()

            if not candidate_fp:
                continue

            d = self.distance(fingerprint, candidate_fp)

            if d <= best_distance:
                best = candidate
                best_distance = d

        if best is None:
            return None

        return (best, best_distance)
