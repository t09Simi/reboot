"""
Trend aggregation service.

Reads RawJobListing rows from a recent time window and produces JobTrend
rows for skills, roles, and companies. Each run creates a new snapshot —
historical snapshots are preserved so we can compute growth and show
long-term trend charts.

Usage:
    from trends.services.aggregator import compute_trends_snapshot
    summary = compute_trends_snapshot(window_days=7, top_n=20)
"""

from collections import Counter
from datetime import timedelta
from typing import Optional

from django.db import transaction
from django.utils import timezone

from concepts.models import Skill
from trends.models import RawJobListing, JobTrend
from trends.services.skill_extractor import extract_skill_ids


# Default knobs — exposed via function args, defined here for clarity.
DEFAULT_WINDOW_DAYS = 7
DEFAULT_TOP_N = 20
GROWTH_LOOKBACK_DAYS = 7


# ---------------------------------------------------------------------------
# Counting helpers — each returns a Counter keyed by display name.
# Kept separate so the canonicalisation layer for roles can be swapped later
# without touching skill/company logic.
# ---------------------------------------------------------------------------

def _count_skills(listings) -> tuple[Counter, dict[str, int]]:
    """
    Returns (counter_by_name, skill_id_by_name).
    Document-level counting: one vote per listing per skill.
    """
    counter: Counter = Counter()
    id_by_name: dict[str, int] = {}

    # Cache the id→name lookup once so we don't hit DB per listing.
    skill_lookup = {s.id: s.name for s in Skill.objects.only('id', 'name')}

    for listing in listings:
        skill_ids = extract_skill_ids(listing.job_description)
        for sid in skill_ids:
            name = skill_lookup.get(sid)
            if not name:
                continue
            counter[name] += 1
            id_by_name[name] = sid

    return counter, id_by_name


def _count_roles(listings) -> Counter:
    """
    Counts raw `job_title` strings as-is.

    NOTE: For now this counts raw titles. Real-world data has variants
    ('Senior Python Developer', 'Sr. Python Developer', etc.) that would
    fragment counts. When we wire up JSearch, add a normalisation step
    here that maps to canonical concepts.JobRole entries.
    """
    return Counter(listing.job_title for listing in listings if listing.job_title)


def _count_companies(listings) -> Counter:
    """One vote per listing per employer."""
    return Counter(
        listing.employer_name for listing in listings
        if listing.employer_name
    )


# ---------------------------------------------------------------------------
# Growth lookup
# ---------------------------------------------------------------------------

def _previous_percentage(
    trend_type: str,
    name: str,
    current_snapshot_date,
) -> Optional[float]:
    """
    Returns the most recent prior percentage for this (trend_type, name)
    within roughly the last week. Slightly wider than 7 days to tolerate
    snapshots that are a day late or early.
    """
    # Look back up to (and including) GROWTH_LOOKBACK_DAYS ago.
# Without the +1, a snapshot exactly 7 days old falls outside the window.
    cutoff = current_snapshot_date - timedelta(days=GROWTH_LOOKBACK_DAYS + 1)

    prior = (
        JobTrend.objects
        .filter(
            trend_type=trend_type,
            name=name,
            snapshot_date__lt=current_snapshot_date,
            snapshot_date__gte=cutoff,
        )
        .order_by('-snapshot_date')
        .values_list('percentage', flat=True)
        .first()
    )
    return prior


def _growth_pct(current: float, prior: Optional[float]) -> Optional[float]:
    """
    Percentage-point change from `prior` to `current`.
    Returns None when prior is unknown — never fabricates a 0.

    Note: this is percentage-point change, not relative change.
    'Python went from 75% to 78%' → +3.0 (percentage points), not +4%.
    Percentage points are the right unit for share-of-listings trends.
    """
    if prior is None:
        return None
    return round(current - prior, 2)


# ---------------------------------------------------------------------------
# Per-trend-type writers
# ---------------------------------------------------------------------------

def _write_trends(
    trend_type: str,
    counter: Counter,
    sample_size: int,
    snapshot_date,
    top_n: int,
    skill_id_by_name: Optional[dict[str, int]] = None,
) -> int:
    """
    Writes the top-N entries from `counter` as JobTrend rows.
    Returns the number of rows written.
    """
    if sample_size == 0 or not counter:
        return 0

    rows = []
    for name, count in counter.most_common(top_n):
        percentage = round((count / sample_size) * 100, 2)
        prior = _previous_percentage(trend_type, name, snapshot_date)
        growth = _growth_pct(percentage, prior)

        rows.append(JobTrend(
            trend_type=trend_type,
            name=name,
            skill_id=(skill_id_by_name or {}).get(name),
            count=count,
            percentage=percentage,
            growth_7d=growth,
            snapshot_date=snapshot_date,
            sample_size=sample_size,
        ))

    JobTrend.objects.bulk_create(rows)
    return len(rows)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

@transaction.atomic
def compute_trends_snapshot(
    window_days: int = DEFAULT_WINDOW_DAYS,
    top_n: int = DEFAULT_TOP_N,
    snapshot_date=None,
) -> dict:
    """
    Compute one snapshot of trends over the last `window_days` days
    of listings, writing top-N rows for each trend type.

    Idempotent within a single day: if a snapshot for today already exists,
    it is replaced (delete then re-insert) so re-running picks up new
    listings without duplicating rows.

    Returns a summary dict for logging.
    """
    snapshot_date = snapshot_date or timezone.now().date()
    window_start = timezone.now() - timedelta(days=window_days)

    listings = list(
        RawJobListing.objects
        .filter(job_posted_at__gte=window_start)
        .only('job_title', 'employer_name', 'job_description')
    )
    sample_size = len(listings)

    # Replace any existing snapshot for this date — keeps re-runs idempotent.
    JobTrend.objects.filter(snapshot_date=snapshot_date).delete()

    if sample_size == 0:
        return {
            'snapshot_date': snapshot_date,
            'sample_size': 0,
            'skills_written': 0,
            'roles_written': 0,
            'companies_written': 0,
            'note': 'No listings in window — nothing to aggregate.',
        }

    skill_counter, skill_ids = _count_skills(listings)
    role_counter = _count_roles(listings)
    company_counter = _count_companies(listings)

    skills_written = _write_trends(
        JobTrend.TrendType.SKILL, skill_counter, sample_size,
        snapshot_date, top_n, skill_id_by_name=skill_ids,
    )
    roles_written = _write_trends(
        JobTrend.TrendType.ROLE, role_counter, sample_size,
        snapshot_date, top_n,
    )
    companies_written = _write_trends(
        JobTrend.TrendType.COMPANY, company_counter, sample_size,
        snapshot_date, top_n,
    )

    return {
        'snapshot_date': snapshot_date,
        'sample_size': sample_size,
        'window_days': window_days,
        'skills_written': skills_written,
        'roles_written': roles_written,
        'companies_written': companies_written,
    }