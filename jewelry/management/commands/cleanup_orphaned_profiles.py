from django.core.management.base import BaseCommand
from jewelry.models import UserProfile


class Command(BaseCommand):
    help = "Find and clean up orphaned profiles (profiles without associated users)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--fix",
            action="store_true",
            help="Actually delete orphaned profiles (default is check-only)",
        )

    def handle(self, *args, **options):
        fix = options.get("fix", False)

        # Find orphaned profiles
        orphaned_profiles = []
        for profile in UserProfile.objects.all():
            try:
                # Try to access the user - if it doesn't exist, this will raise an exception
                profile.user
            except Exception:
                orphaned_profiles.append(profile)

        if not orphaned_profiles:
            self.stdout.write(self.style.SUCCESS("No orphaned profiles found. All profiles have valid users."))
            return

        self.stdout.write(f"Found {len(orphaned_profiles)} orphaned profiles:")
        self.stdout.write("-" * 80)
        
        for profile in orphaned_profiles:
            self.stdout.write(f"Profile ID: {profile.id}, Created: {profile.created_at}")

        if not fix:
            self.stdout.write(self.style.WARNING("\nThis was a check-only run. Use --fix to delete orphaned profiles."))
            return

        # Ask for confirmation
        confirm = input(f"\nThis will DELETE {len(orphaned_profiles)} orphaned profiles. Are you sure? (yes/no): ")
        if confirm.lower() != "yes":
            self.stdout.write(self.style.WARNING("Operation cancelled."))
            return

        deleted_count = 0
        for profile in orphaned_profiles:
            try:
                profile.delete()
                deleted_count += 1
                self.stdout.write(f"Deleted orphaned profile ID: {profile.id}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error deleting profile ID {profile.id}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully deleted {deleted_count} orphaned profiles.")) 