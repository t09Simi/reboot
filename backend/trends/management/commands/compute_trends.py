"""
Run one trend aggregation snapshot.

Examples:
    python manage.py compute_trends
    python manage.py compute_trends --window 14 --top 30
"""

from django.core.management.base import BaseCommand

from trends.services.aggregator import compute_trends_snapshot


class Command(BaseCommand):
    help = "Compute one snapshot of job trends from RawJobListing data."

    def add_arguments(self, parser):
        parser.add_argument(
            '--window', type=int, default=7,
            help='Aggregate listings posted in the last N days (default: 7).',
        )
        parser.add_argument(
            '--top', type=int, default=20,
            help='Top N entries per trend type (default: 20).',
        )

    def handle(self, *args, **options):
        summary = compute_trends_snapshot(
            window_days=options['window'],
            top_n=options['top'],
        )

        self.stdout.write(self.style.SUCCESS(
            f"Snapshot {summary['snapshot_date']}: "
            f"{summary['sample_size']} listings, "
            f"wrote {summary['skills_written']} skill trends, "
            f"{summary['roles_written']} role trends, "
            f"{summary['companies_written']} company trends."
        ))