import logging

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand
from django.utils import timezone

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Reset authentication for a specific user"

    def add_arguments(self, parser):
        parser.add_argument(
            "email", type=str, help="Email of the user to reset authentication for"
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force reset without confirmation",
        )

    def handle(self, *args, **options):
        email = options["email"]

        if not options["force"]:
            confirm = input(
                f"This will reset authentication for {email}. Are you sure? (yes/no): "
            )
            if confirm.lower() != "yes":
                self.stdout.write(self.style.WARNING("Operation cancelled."))
                return

        try:
            # Find the user
            user = User.objects.get(email=email)
            self.stdout.write(f"Found user: {user.email} (ID: {user.id})")

            # Clear all sessions for this user
            sessions = Session.objects.all()
            deleted_sessions = 0

            for session in sessions:
                try:
                    session_data = session.get_decoded()
                    session_user_id = session_data.get("_auth_user_id")

                    if session_user_id and str(session_user_id) == str(user.id):
                        session.delete()
                        deleted_sessions += 1
                        self.stdout.write(f"Deleted session: {session.session_key}")
                except Exception as e:
                    self.stdout.write(f"Error processing session: {str(e)}")

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully deleted {deleted_sessions} sessions for user {email}"
                )
            )

            # Optionally deactivate the user temporarily
            if not options["force"]:
                deactivate = input(
                    "Do you want to temporarily deactivate this user? (yes/no): "
                )
                if deactivate.lower() == "yes":
                    user.is_active = False
                    user.save()
                    self.stdout.write(
                        self.style.WARNING(f"User {email} has been deactivated")
                    )

        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User with email {email} not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
