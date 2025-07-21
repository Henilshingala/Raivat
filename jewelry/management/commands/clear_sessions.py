from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Clear all user sessions"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be deleted without actually deleting",
        )

    def handle(self, *args, **options):
        session_count = Session.objects.count()

        if options["dry_run"]:
            self.stdout.write(
                self.style.WARNING(f"DRY RUN: Would delete {session_count} sessions")
            )
            return

        if session_count > 0:
            Session.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS(f"Successfully cleared {session_count} sessions")
            )
        else:
            self.stdout.write(self.style.SUCCESS("No sessions found to clear"))
