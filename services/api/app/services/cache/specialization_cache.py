from functools import lru_cache
from typing import List


@lru_cache(maxsize=256)
def _cached_slug(slug: str) -> str:
    return slug


def normalize_slug(name: str) -> str:
    return _cached_slug(name.strip().lower())


def bulk_normalize(slugs: List[str]) -> List[str]:
    return [normalize_slug(s) for s in slugs]