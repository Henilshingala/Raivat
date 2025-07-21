from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from jewelry.models import UserProfile


class Command(BaseCommand):
    help = "Clean up inactive users and their profiles"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be deleted without actually deleting",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        # Find inactive users
        inactive_users = User.objects.filter(is_active=False)

        if not inactive_users.exists():
            self.stdout.write(self.style.SUCCESS("No inactive users found."))
            return

        self.stdout.write(f"Found {inactive_users.count()} inactive users.")

        if dry_run:
            self.stdout.write("DRY RUN - No changes will be made.")

        deleted_count = 0

        for user in inactive_users:
            try:
                self.stdout.write(f"Processing user: {user.email} (ID: {user.id})")

                if not dry_run:
                    # Delete user profile first
                    try:
                        profile = user.profile
                        profile.delete()
                        self.stdout.write(f"  - Deleted profile for {user.email}")
                    except UserProfile.DoesNotExist:
                        self.stdout.write(f"  - No profile found for {user.email}")

                    # Delete the user
                    user.delete()
                    deleted_count += 1
                    self.stdout.write(f"  - Deleted user {user.email}")
                else:
                    self.stdout.write(f"  - Would delete user {user.email}")

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error processing user {user.email}: {str(e)}")
                )

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"DRY RUN: Would have deleted {deleted_count} users."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully deleted {deleted_count} inactive users."
                )
            )
