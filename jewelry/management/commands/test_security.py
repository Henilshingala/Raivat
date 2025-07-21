import logging

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import reverse

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Test the security system to ensure authentication is bulletproof"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🔒 Testing Security System..."))

        # Test 1: Check for any invalid sessions
        self._test_session_integrity()

        # Test 2: Check for any inactive users with sessions
        self._test_user_status()

        # Test 3: Test authentication middleware
        self._test_authentication_middleware()

        self.stdout.write(self.style.SUCCESS("✅ Security tests completed!"))

    def _test_session_integrity(self):
        """Test session integrity"""
        self.stdout.write("Testing session integrity...")

        sessions = Session.objects.all()
        invalid_sessions = 0

        for session in sessions:
            try:
                session_data = session.get_decoded()
                user_id = session_data.get("_auth_user_id")

                if user_id:
                    # Check if user exists and is active
                    try:
                        user = User.objects.get(id=user_id, is_active=True)
                    except User.DoesNotExist:
                        invalid_sessions += 1
                        self.stdout.write(
                            self.style.WARNING(
                                f"Invalid session found: User {user_id} does not exist or is inactive"
                            )
                        )
            except Exception as e:
                invalid_sessions += 1
                self.stdout.write(
                    self.style.WARNING(f"Corrupted session found: {str(e)}")
                )

        if invalid_sessions == 0:
            self.stdout.write(self.style.SUCCESS("✅ All sessions are valid"))
        else:
            self.stdout.write(
                self.style.WARNING(f"⚠️ Found {invalid_sessions} invalid sessions")
            )

    def _test_user_status(self):
        """Test user status"""
        self.stdout.write("Testing user status...")

        inactive_users = User.objects.filter(is_active=False)
        if inactive_users.exists():
            self.stdout.write(
                self.style.WARNING(f"⚠️ Found {inactive_users.count()} inactive users")
            )
            for user in inactive_users:
                self.stdout.write(f"  - {user.email} (ID: {user.id})")
        else:
            self.stdout.write(self.style.SUCCESS("✅ All users are active"))

    def _test_authentication_middleware(self):
        """Test authentication middleware"""
        self.stdout.write("Testing authentication middleware...")

        client = Client()

        # Test 1: Try to access account page without authentication
        response = client.get(reverse("account"))
        if response.status_code == 302 and "login" in response.url:
            self.stdout.write(
                self.style.SUCCESS("✅ Unauthenticated access properly redirected")
            )
        else:
            self.stdout.write(
                self.style.ERROR("❌ Unauthenticated access not properly handled")
            )

        # Test 2: Try to access account page with invalid session
        client.session["_auth_user_id"] = 99999  # Non-existent user
        response = client.get(reverse("account"))
        if response.status_code == 302 and "login" in response.url:
            self.stdout.write(self.style.SUCCESS("✅ Invalid session properly handled"))
        else:
            self.stdout.write(
                self.style.ERROR("❌ Invalid session not properly handled")
            )
