import logging
from datetime import timedelta

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand
from django.utils import timezone

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Monitor security status and automatically fix issues"

    def add_arguments(self, parser):
        parser.add_argument(
            "--fix",
            action="store_true",
            help="Automatically fix security issues found",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Show detailed information",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🔒 Security Monitor Starting..."))

        issues_found = 0

        # Check 1: Invalid sessions
        issues_found += self._check_invalid_sessions(options["fix"], options["verbose"])

        # Check 2: Expired sessions
        issues_found += self._check_expired_sessions(options["fix"], options["verbose"])

        # Check 3: Inactive users with sessions
        issues_found += self._check_inactive_users(options["fix"], options["verbose"])

        # Check 4: Orphaned sessions
        issues_found += self._check_orphaned_sessions(
            options["fix"], options["verbose"]
        )

        if issues_found == 0:
            self.stdout.write(self.style.SUCCESS("✅ No security issues found!"))
        else:
            self.stdout.write(
                self.style.WARNING(f"⚠️ Found {issues_found} security issues")
            )
            if not options["fix"]:
                self.stdout.write(
                    self.style.WARNING("Run with --fix to automatically resolve issues")
                )

    def _check_invalid_sessions(self, fix=False, verbose=False):
        """Check for sessions with invalid user IDs"""
        issues = 0
        sessions = Session.objects.all()

        for session in sessions:
            try:
                session_data = session.get_decoded()
                user_id = session_data.get("_auth_user_id")

                if user_id:
                    try:
                        user = User.objects.get(id=user_id, is_active=True)
                    except User.DoesNotExist:
                        issues += 1
                        if verbose:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Invalid session: User {user_id} not found"
                                )
                            )
                        if fix:
                            session.delete()
                            if verbose:
                                self.stdout.write(f"  → Deleted invalid session")
            except Exception as e:
                issues += 1
                if verbose:
                    self.stdout.write(
                        self.style.WARNING(f"Corrupted session: {str(e)}")
                    )
                if fix:
                    session.delete()
                    if verbose:
                        self.stdout.write(f"  → Deleted corrupted session")

        if issues == 0:
            self.stdout.write(self.style.SUCCESS("✅ All sessions are valid"))
        else:
            self.stdout.write(self.style.WARNING(f"⚠️ Found {issues} invalid sessions"))

        return issues

    def _check_expired_sessions(self, fix=False, verbose=False):
        """Check for expired sessions (older than 2 weeks)"""
        issues = 0
        two_weeks_ago = timezone.now() - timedelta(days=14)
        expired_sessions = Session.objects.filter(expire_date__lt=two_weeks_ago)

        if expired_sessions.exists():
            issues = expired_sessions.count()
            if verbose:
                self.stdout.write(
                    self.style.WARNING(f"Found {issues} expired sessions")
                )
            if fix:
                expired_sessions.delete()
                if verbose:
                    self.stdout.write(f"  → Deleted {issues} expired sessions")
        else:
            self.stdout.write(self.style.SUCCESS("✅ No expired sessions found"))

        return issues

    def _check_inactive_users(self, fix=False, verbose=False):
        """Check for inactive users"""
        issues = 0
        inactive_users = User.objects.filter(is_active=False)

        if inactive_users.exists():
            issues = inactive_users.count()
            if verbose:
                self.stdout.write(self.style.WARNING(f"Found {issues} inactive users"))
                for user in inactive_users:
                    self.stdout.write(f"  - {user.email} (ID: {user.id})")
        else:
            self.stdout.write(self.style.SUCCESS("✅ All users are active"))

        return issues

    def _check_orphaned_sessions(self, fix=False, verbose=False):
        """Check for sessions without user data"""
        issues = 0
        sessions = Session.objects.all()

        for session in sessions:
            try:
                session_data = session.get_decoded()
                if not session_data.get("_auth_user_id") and len(session_data) > 0:
                    issues += 1
                    if verbose:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Orphaned session: {session.session_key}"
                            )
                        )
                    if fix:
                        session.delete()
                        if verbose:
                            self.stdout.write(f"  → Deleted orphaned session")
            except Exception:
                issues += 1
                if verbose:
                    self.stdout.write(
                        self.style.WARNING(f"Unreadable session: {session.session_key}")
                    )
                if fix:
                    session.delete()
                    if verbose:
                        self.stdout.write(f"  → Deleted unreadable session")

        if issues == 0:
            self.stdout.write(self.style.SUCCESS("✅ No orphaned sessions found"))
        else:
            self.stdout.write(self.style.WARNING(f"⚠️ Found {issues} orphaned sessions"))

        return issues
