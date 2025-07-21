from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from jewelry.models import UserProfile


class Command(BaseCommand):
    help = "Find and fix users who are missing profiles"

    def add_arguments(self, parser):
        parser.add_argument(
            "--fix",
            action="store_true",
            help="Actually create missing profiles (default is check-only)",
        )
        parser.add_argument(
            "--delete-users",
            action="store_true",
            help="Delete users who are missing profiles instead of creating profiles",
        )

    def handle(self, *args, **options):
        fix = options.get("fix", False)
        delete_users = options.get("delete_users", False)

        # Find users without profiles
        users_without_profiles = []
        for user in User.objects.all():
            try:
                user.profile
            except UserProfile.DoesNotExist:
                users_without_profiles.append(user)

        if not users_without_profiles:
            self.stdout.write(self.style.SUCCESS("All users have profiles. No issues found."))
            return

        self.stdout.write(f"Found {len(users_without_profiles)} users without profiles:")
        self.stdout.write("-" * 80)
        
        for user in users_without_profiles:
            self.stdout.write(f"ID: {user.id}, Email: {user.email}, Username: {user.username}, Active: {user.is_active}")

        if not fix and not delete_users:
            self.stdout.write(self.style.WARNING("\nThis was a check-only run. Use --fix to create missing profiles or --delete-users to delete users without profiles."))
            return

        if delete_users:
            if not fix:  # Ask for confirmation
                confirm = input(f"\nThis will DELETE {len(users_without_profiles)} users without profiles. Are you sure? (yes/no): ")
                if confirm.lower() != "yes":
                    self.stdout.write(self.style.WARNING("Operation cancelled."))
                    return

            deleted_count = 0
            for user in users_without_profiles:
                try:
                    user.delete()
                    deleted_count += 1
                    self.stdout.write(f"Deleted user: {user.email}")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error deleting user {user.email}: {str(e)}"))

            self.stdout.write(self.style.SUCCESS(f"Successfully deleted {deleted_count} users without profiles."))

        elif fix:
            created_count = 0
            for user in users_without_profiles:
                try:
                    UserProfile.objects.create(user=user)
                    created_count += 1
                    self.stdout.write(f"Created profile for user: {user.email}")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creating profile for user {user.email}: {str(e)}"))

            self.stdout.write(self.style.SUCCESS(f"Successfully created {created_count} missing profiles.")) 