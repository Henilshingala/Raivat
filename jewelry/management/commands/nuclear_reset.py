import logging

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.utils import timezone

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Nuclear reset - completely clear all sessions, cache, and reset authentication"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force nuclear reset without confirmation",
        )

    def handle(self, *args, **options):
        if not options["force"]:
            self.stdout.write(self.style.WARNING("⚠️  NUCLEAR RESET WARNING ⚠️"))
            self.stdout.write("This will:")
            self.stdout.write("1. Clear ALL user sessions")
            self.stdout.write("2. Clear ALL cache")
            self.stdout.write("3. Reset ALL authentication")
            self.stdout.write("4. Force ALL users to log in again")
            self.stdout.write("")
            confirm = input('Type "NUCLEAR" to confirm: ')
            if confirm != "NUCLEAR":
                self.stdout.write(self.style.WARNING("Nuclear reset cancelled."))
                return

        self.stdout.write(self.style.SUCCESS("🚀 Starting Nuclear Reset..."))

        # Step 1: Clear all sessions
        session_count = Session.objects.count()
        Session.objects.all().delete()
        self.stdout.write(f"✅ Cleared {session_count} sessions")

        # Step 2: Clear all cache
        cache.clear()
        self.stdout.write("✅ Cleared all cache")

        # Step 3: Log all users out by updating their last_login
        users = User.objects.filter(is_active=True)
        for user in users:
            user.last_login = None
            user.save()
        self.stdout.write(f"✅ Reset last_login for {users.count()} users")

        # Step 4: Clear any potential session data
        try:
            from django.contrib.sessions.backends.db import SessionStore

            SessionStore().clear()
            self.stdout.write("✅ Cleared session store")
        except:
            pass

        # Step 5: Force garbage collection
        import gc

        gc.collect()
        self.stdout.write("✅ Forced garbage collection")

        self.stdout.write(self.style.SUCCESS("🎉 Nuclear Reset Complete!"))
        self.stdout.write("All users must now log in again.")
        self.stdout.write("All cached data has been cleared.")
        self.stdout.write("All sessions have been destroyed.")
