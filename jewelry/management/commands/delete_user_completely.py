import logging

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand
from jewelry.models import UserDiscount, UserProfile

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Completely delete a user and all related data"

    def add_arguments(self, parser):
        parser.add_argument(
            "email", type=str, help="Email of the user to completely delete"
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force deletion without confirmation",
        )

    def handle(self, *args, **options):
        email = options["email"]

        if not options["force"]:
            confirm = input(
                f"This will COMPLETELY delete user {email} and ALL related data. Are you sure? (yes/no): "
            )
            if confirm.lower() != "yes":
                self.stdout.write(self.style.WARNING("Operation cancelled."))
                return

        try:
            # Find the user
            user = User.objects.get(email=email)
            self.stdout.write(f"Found user: {user.email} (ID: {user.id})")

            # Step 1: Delete all sessions for this user
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

            self.stdout.write(f"Deleted {deleted_sessions} sessions")

            # Step 2: Delete UserDiscount records
            try:
                user_discounts = UserDiscount.objects.filter(user=user)
                discount_count = user_discounts.count()
                user_discounts.delete()
                self.stdout.write(f"Deleted {discount_count} user discount records")
            except Exception as e:
                self.stdout.write(f"Error deleting user discounts: {str(e)}")

            # Step 3: Delete UserProfile
            try:
                profile = UserProfile.objects.get(user=user)
                profile.delete()
                self.stdout.write("Deleted user profile")
            except UserProfile.DoesNotExist:
                self.stdout.write("No user profile found")
            except Exception as e:
                self.stdout.write(f"Error deleting user profile: {str(e)}")

            # Step 4: Delete the user completely
            user.delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully deleted user {email} and all related data"
                )
            )

        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User with email {email} not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
