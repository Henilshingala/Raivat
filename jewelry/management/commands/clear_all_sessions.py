from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Clear all user sessions to fix authentication issues"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force clear all sessions without confirmation",
        )

    def handle(self, *args, **options):
        if not options["force"]:
            confirm = input("This will log out ALL users. Are you sure? (yes/no): ")
            if confirm.lower() != "yes":
                self.stdout.write(self.style.WARNING("Operation cancelled."))
                return

        # Clear all sessions
        deleted_count = Session.objects.all().delete()[0]

        self.stdout.write(
            self.style.SUCCESS(f"Successfully cleared {deleted_count} user sessions.")
        )
        self.stdout.write(self.style.SUCCESS("All users will need to log in again."))
