"""
Generates realistic mock RawJobListing rows for development.

Designed so that:
- Skills appear with realistic frequency (some popular, some rare)
- Listings span the last N days for time-window trend testing
- Output is deterministic by default (--seed) for reproducible debugging
"""

import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from trends.models import RawJobListing


# ---------------------------------------------------------------------------
# Mock data fragments
# Skills are weighted: higher weight = appears in more listings.
# This mimics real job market distribution where Python/React/AWS dominate.
# ---------------------------------------------------------------------------

# (skill_phrase, weight) — phrase is what gets embedded in the description.
# We deliberately mix canonical and alias forms to test the extractor.
SKILL_POOL = [
    # Top tier — appear in ~60-80% of relevant listings
    ("Python", 80), ("JavaScript", 75), ("React", 70), ("AWS", 65),
    ("SQL", 65), ("Git", 70), ("REST APIs", 60),
    # Mid tier — ~30-50%
    ("Docker", 50), ("PostgreSQL", 45), ("TypeScript", 40), ("Node.js", 40),
    ("Django", 35), ("Kubernetes", 30), ("CI/CD", 35), ("Linux", 40),
    ("MongoDB", 30), ("Redis", 25), ("Java", 35),
    # Lower tier — ~10-25%
    ("FastAPI", 20), ("Flask", 18), ("Spring Boot", 22), ("GraphQL", 18),
    ("Terraform", 15), ("Jenkins", 18), ("GitHub Actions", 20), ("Pytest", 15),
    ("Tailwind CSS", 22), ("Next.js", 25), ("Vue", 15), ("Angular", 15),
    ("Microservices", 20), ("Agile", 30), ("Scrum", 25), ("TDD", 12),
    # Niche — ~5-10%
    ("Kafka", 10), ("Airflow", 8), ("Spark", 10), ("Elasticsearch", 8),
    ("Rust", 5), ("Go", 12), ("Kotlin", 8), ("Scala", 5),
    ("LangChain", 8), ("LLMs", 10), ("TensorFlow", 7), ("PyTorch", 8),
    ("Snowflake", 6), ("Databricks", 5),
]

# Job roles — weighted by how common they are
ROLE_POOL = [
    ("Software Engineer", 30), ("Backend Developer", 25), ("Frontend Developer", 25),
    ("Full Stack Developer", 20), ("Senior Software Engineer", 18),
    ("Python Developer", 15), ("React Developer", 12), ("DevOps Engineer", 15),
    ("Data Engineer", 12), ("Junior Software Developer", 10),
    ("Software Development Engineer", 8), ("Machine Learning Engineer", 8),
    ("Cloud Engineer", 8), ("Site Reliability Engineer", 6),
    ("Mobile Developer", 6), ("QA Engineer", 7), ("Engineering Manager", 5),
]

COMPANIES = [
    "Infosys", "TCS", "Wipro", "Tech Mahindra", "Accenture", "Cognizant",
    "Razorpay", "Zerodha", "Swiggy", "Zomato", "Flipkart", "PhonePe",
    "Freshworks", "Postman", "Atlan", "Cred", "Meesho", "BrowserStack",
    "Microsoft", "Amazon", "Google", "Adobe", "Walmart Labs", "Uber",
    "Stripe India", "Salesforce", "ThoughtSpot", "Hasura", "Druva",
]

CITIES_IN = [
    ("Bengaluru", "IN"), ("Mumbai", "IN"), ("Pune", "IN"), ("Hyderabad", "IN"),
    ("Chennai", "IN"), ("Gurgaon", "IN"), ("Noida", "IN"), ("Remote", "IN"),
]

# Templates — {role}, {skills_list}, {company} get filled in.
# Multiple templates so listings don't all look identical.
DESCRIPTION_TEMPLATES = [
    (
        "We are hiring a {role} to join our team at {company}. "
        "The ideal candidate has strong experience with {skills_list}. "
        "You will work on building scalable systems, collaborating with cross-functional teams, "
        "and shipping production-grade code. Familiarity with modern engineering practices is a plus."
    ),
    (
        "{company} is looking for a {role} who can hit the ground running. "
        "Required skills include {skills_list}. "
        "Responsibilities include designing APIs, writing tests, conducting code reviews, "
        "and mentoring junior team members. Bonus points for open-source contributions."
    ),
    (
        "Join {company} as a {role}. "
        "You should be comfortable working with {skills_list} in a fast-paced environment. "
        "We value clean code, good documentation, and a collaborative engineering culture. "
        "Remote-friendly with quarterly team meetups."
    ),
    (
        "Position: {role} at {company}. "
        "Tech stack: {skills_list}. "
        "You'll own features end-to-end — from design to deployment to monitoring. "
        "We're a small team, so impact per engineer is high."
    ),
    (
        "{company} engineering is expanding. We need a {role} with hands-on experience in {skills_list}. "
        "The role involves architecting new services, scaling existing ones, "
        "and contributing to engineering best practices across the org."
    ),
]


def weighted_choice(pool, k=None):
    """Pick `k` items from `[(item, weight), ...]` without replacement, weighted."""
    items, weights = zip(*pool)
    if k is None:
        return random.choices(items, weights=weights, k=1)[0]
    # For sampling without replacement, we do it the slow but correct way
    chosen = []
    remaining = list(pool)
    for _ in range(min(k, len(remaining))):
        items, weights = zip(*remaining)
        pick = random.choices(items, weights=weights, k=1)[0]
        chosen.append(pick)
        remaining = [(i, w) for i, w in remaining if i != pick]
    return chosen


def fake_salary_range():
    """Return (min, max) in INR or (None, None) for ~30% of listings."""
    if random.random() < 0.3:
        return None, None
    base = random.choice([600_000, 900_000, 1_200_000, 1_800_000, 2_400_000, 3_000_000])
    spread = random.randint(300_000, 800_000)
    return base, base + spread


class Command(BaseCommand):
    help = "Seed the RawJobListing table with realistic mock data for development."

    def add_arguments(self, parser):
        parser.add_argument(
            '--count', type=int, default=200,
            help='Number of mock listings to create (default: 200).'
        )
        parser.add_argument(
            '--days', type=int, default=30,
            help='Spread listings across the last N days (default: 30).'
        )
        parser.add_argument(
            '--seed', type=int, default=42,
            help='Random seed for reproducibility (default: 42). Use 0 for true randomness.'
        )
        parser.add_argument(
            '--wipe', action='store_true',
            help='Delete existing RawJobListings before seeding.'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['seed']:
            random.seed(options['seed'])

        if options['wipe']:
            deleted, _ = RawJobListing.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing listings."))

        count = options['count']
        days = options['days']
        now = timezone.now()

        listings_to_create = []
        for i in range(count):
            role = weighted_choice(ROLE_POOL)
            company = random.choice(COMPANIES)
            city, country = random.choice(CITIES_IN)

            # Pick 4-9 skills per listing, weighted by popularity
            num_skills = random.randint(4, 9)
            skills = weighted_choice(SKILL_POOL, k=num_skills)
            skills_list = ", ".join(skills)

            template = random.choice(DESCRIPTION_TEMPLATES)
            description = template.format(
                role=role, company=company, skills_list=skills_list
            )

            min_salary, max_salary = fake_salary_range()

            # Posted some random time in the last `days` days
            offset_seconds = random.randint(0, days * 86400)
            posted_at = now - timedelta(seconds=offset_seconds)

            listings_to_create.append(RawJobListing(
                job_id=f"mock-{options['seed']}-{i:05d}",
                job_title=role,
                employer_name=company,
                job_city=city,
                job_country=country,
                job_description=description,
                job_posted_at=posted_at,
                job_min_salary=min_salary,
                job_max_salary=max_salary,
            ))

        # bulk_create is dramatically faster than 200 individual saves
        RawJobListing.objects.bulk_create(listings_to_create, ignore_conflicts=True)

        actual = RawJobListing.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f"Created {len(listings_to_create)} mock listings. "
            f"Total in DB: {actual}."
        ))