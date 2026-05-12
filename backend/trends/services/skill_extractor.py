"""
Skill extraction service.

Matches canonical Skills against job descriptions using regex with custom
boundary rules:

- Default boundary (alphanumerics only) — works correctly for skills with
  special characters like C++, C#, .NET, Node.js. The skill 'C++' matches
  in 'We use C++,' but not in 'sequence ABCC++'.
- Strict boundary (alphanumerics + . - /) — used for short aliases (≤3 chars)
  like 'js', 'ts', 'py'. Prevents matches inside compound terms like 'react.js'
  or 'node-js'.
- Ambiguity filter — skills whose names collide with English words ('Swift',
  'Go', 'Rust', 'R') only match if a context keyword also appears.
"""

import re
from functools import lru_cache

from concepts.models import Skill


# Default boundary: don't match if adjacent to alphanumeric.
# Allows 'C++' to match next to spaces, commas, etc.
_DEFAULT_BOUNDARY = r"A-Za-z0-9"

# Strict boundary for short aliases: also disallow period, hyphen, slash.
# Prevents 'js' from matching in 'react.js' or 'node-js'.
_STRICT_BOUNDARY = r"A-Za-z0-9.\-/"

# Aliases at or below this length use the strict boundary.
_STRICT_BOUNDARY_MAX_LEN = 3


# Skills whose names/aliases collide with common English words.
# To match, the description must also contain a context keyword.
# Keys are Skill.slug values.
AMBIGUOUS_SKILLS: dict[str, list[str]] = {
    'swift':  ['ios', 'xcode', 'macos', 'apple', 'iphone', 'objective-c', 'cocoa'],
    'go':     ['golang', 'goroutine', 'gopher'],
    'r-lang': ['rstudio', 'tidyverse', 'ggplot', 'cran', 'data analysis', 'statistics', 'statistical'],
    'rust':   ['cargo', 'rustc', 'systems programming'],
}


def _build_pattern(phrase: str) -> str:
    """
    Build a regex pattern for `phrase`.

    Short phrases use a strict boundary that excludes . - / so they don't
    match inside compound terms (react.js, node-js). Longer phrases use
    the default boundary that handles special characters in the phrase
    itself (C++, .NET).
    """
    escaped = re.escape(phrase)
    boundary = _STRICT_BOUNDARY if len(phrase) <= _STRICT_BOUNDARY_MAX_LEN else _DEFAULT_BOUNDARY
    return rf"(?<![{boundary}]){escaped}(?![{boundary}])"


def _build_skill_patterns() -> list[tuple[int, str, re.Pattern]]:
    """Returns (skill_id, skill_slug, compiled_regex) for every Skill."""
    patterns: list[tuple[int, str, re.Pattern]] = []

    for skill in Skill.objects.all().only('id', 'slug', 'name', 'aliases'):
        phrases = [skill.name] + list(skill.aliases or [])
        # Sort longest-first so 'Spring Boot' is tested before 'Spring',
        # avoiding partial matches in the alternation.
        phrases = sorted(set(phrases), key=len, reverse=True)
        combined = "|".join(_build_pattern(p) for p in phrases)
        compiled = re.compile(combined, re.IGNORECASE)
        patterns.append((skill.id, skill.slug, compiled))

    return patterns


@lru_cache(maxsize=1)
def get_extractor() -> list[tuple[int, str, re.Pattern]]:
    """
    Cached pattern list. Call `get_extractor.cache_clear()` after seeding new
    skills, or restart the process — otherwise new skills won't be detected.
    """
    return _build_skill_patterns()


def _passes_ambiguity_check(slug: str, description_lower: str) -> bool:
    """For ambiguous skills, require at least one context keyword."""
    context_words = AMBIGUOUS_SKILLS.get(slug)
    if not context_words:
        return True
    return any(ctx in description_lower for ctx in context_words)


def extract_skill_ids(description: str) -> set[int]:
    if not description:
        return set()

    description_lower = description.lower()
    matched: set[int] = set()

    for skill_id, slug, pattern in get_extractor():
        if pattern.search(description) and _passes_ambiguity_check(slug, description_lower):
            matched.add(skill_id)

    return matched


def extract_skills(description: str) -> list[Skill]:
    ids = extract_skill_ids(description)
    if not ids:
        return []
    return list(Skill.objects.filter(id__in=ids))