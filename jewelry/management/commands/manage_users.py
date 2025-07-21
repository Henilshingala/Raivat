from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from jewelry.models import UserProfile, UserDiscount
from django.contrib.sessions.models import Session


class Command(BaseCommand):
    help = "Comprehensive user management tool"

    def add_arguments(self, parser):
        parser.add_argument(
            "action",
            choices=["list", "check", "fix-profiles", "cleanup", "delete"],
            help="Action to perform",
        )
        parser.add_argument(
            "--email",
            type=str,
            help="Email filter for specific user",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force action without confirmation",
        )

    def handle(self, *args, **options):
        action = options["action"]
        email_filter = options.get("email", "")
        force = options.get("force", False)

        if action == "list":
            self.list_users(email_filter)
        elif action == "check":
            self.check_users(email_filter)
        elif action == "fix-profiles":
            self.fix_profiles(force)
        elif action == "cleanup":
            self.cleanup_users(force)
        elif action == "delete":
            if not email_filter:
                self.stdout.write(self.style.ERROR("Email is required for delete action"))
                return
            self.delete_user(email_filter, force)

    def list_users(self, email_filter):
        """List all users with their status"""
        users = User.objects.all()
        if email_filter:
            users = users.filter(email__icontains=email_filter)

        if not users.exists():
            self.stdout.write("No users found.")
            return

        self.stdout.write(f"Found {users.count()} user(s):")
        self.stdout.write("-" * 100)
        self.stdout.write(f"{'ID':<5} {'Email':<35} {'Username':<25} {'Active':<8} {'Staff':<8} {'Has Profile':<12} {'Date Joined'}")
        self.stdout.write("-" * 100)

        for user in users:
            has_profile = "Yes" if hasattr(user, 'profile') else "No"
            self.stdout.write(
                f"{user.id:<5} {user.email:<35} {user.username:<25} {str(user.is_active):<8} {str(user.is_staff):<8} {has_profile:<12} {user.date_joined.strftime('%Y-%m-%d %H:%M')}"
            )

        # Summary
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        inactive_users = User.objects.filter(is_active=False).count()
        
        self.stdout.write("-" * 100)
        self.stdout.write(f"Summary: Total={total_users}, Active={active_users}, Inactive={inactive_users}")

    def check_users(self, email_filter):
        """Check for issues with users"""
        users = User.objects.all()
        if email_filter:
            users = users.filter(email__icontains=email_filter)

        issues_found = False

        for user in users:
            user_issues = []
            
            # Check for missing profile
            try:
                user.profile
            except UserProfile.DoesNotExist:
                user_issues.append("Missing profile")
                issues_found = True

            # Check for active sessions
            sessions = Session.objects.all()
            user_sessions = 0
            for session in sessions:
                try:
                    session_data = session.get_decoded()
                    session_user_id = session_data.get("_auth_user_id")
                    if session_user_id and str(session_user_id) == str(user.id):
                        user_sessions += 1
                except:
                    pass

            if user_sessions > 0:
                user_issues.append(f"{user_sessions} active sessions")

            if user_issues:
                self.stdout.write(f"User {user.email}: {', '.join(user_issues)}")

        if not issues_found:
            self.stdout.write(self.style.SUCCESS("No issues found with users."))

    def fix_profiles(self, force):
        """Fix missing profiles"""
        users_without_profiles = []
        for user in User.objects.all():
            try:
                user.profile
            except UserProfile.DoesNotExist:
                users_without_profiles.append(user)

        if not users_without_profiles:
            self.stdout.write(self.style.SUCCESS("All users have profiles. No fixes needed."))
            return

        self.stdout.write(f"Found {len(users_without_profiles)} users without profiles:")
        for user in users_without_profiles:
            self.stdout.write(f"  - {user.email}")

        if not force:
            confirm = input(f"\nCreate profiles for {len(users_without_profiles)} users? (yes/no): ")
            if confirm.lower() != "yes":
                self.stdout.write("Operation cancelled.")
                return

        created_count = 0
        for user in users_without_profiles:
            try:
                UserProfile.objects.create(user=user)
                created_count += 1
                self.stdout.write(f"Created profile for: {user.email}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating profile for {user.email}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully created {created_count} profiles."))

    def cleanup_users(self, force):
        """Clean up users without profiles"""
        users_without_profiles = []
        for user in User.objects.all():
            try:
                user.profile
            except UserProfile.DoesNotExist:
                users_without_profiles.append(user)

        if not users_without_profiles:
            self.stdout.write(self.style.SUCCESS("No users without profiles found."))
            return

        self.stdout.write(f"Found {len(users_without_profiles)} users without profiles:")
        for user in users_without_profiles:
            self.stdout.write(f"  - {user.email}")

        if not force:
            confirm = input(f"\nDelete {len(users_without_profiles)} users without profiles? (yes/no): ")
            if confirm.lower() != "yes":
                self.stdout.write("Operation cancelled.")
                return

        deleted_count = 0
        for user in users_without_profiles:
            try:
                user.delete()
                deleted_count += 1
                self.stdout.write(f"Deleted user: {user.email}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error deleting user {user.email}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully deleted {deleted_count} users."))

    def delete_user(self, email, force):
        """Delete a specific user completely"""
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User with email {email} not found."))
            return

        self.stdout.write(f"Found user: {user.email} (ID: {user.id})")
        self.stdout.write(f"Username: {user.username}")
        self.stdout.write(f"Is active: {user.is_active}")
        self.stdout.write(f"Is staff: {user.is_staff}")

        if not force:
            confirm = input(f"\nDelete user {email} completely? (yes/no): ")
            if confirm.lower() != "yes":
                self.stdout.write("Operation cancelled.")
                return

        try:
            # Delete sessions
            sessions = Session.objects.all()
            deleted_sessions = 0
            for session in sessions:
                try:
                    session_data = session.get_decoded()
                    session_user_id = session_data.get("_auth_user_id")
                    if session_user_id and str(session_user_id) == str(user.id):
                        session.delete()
                        deleted_sessions += 1
                except:
                    pass

            # Delete user discounts
            user_discounts = UserDiscount.objects.filter(user=user)
            discount_count = user_discounts.count()
            user_discounts.delete()

            # Delete profile
            try:
                profile = user.profile
                profile.delete()
            except UserProfile.DoesNotExist:
                pass

            # Delete user
            user.delete()

            self.stdout.write(self.style.SUCCESS(f"Successfully deleted user {email}"))
            self.stdout.write(f"  - Deleted {deleted_sessions} sessions")
            self.stdout.write(f"  - Deleted {discount_count} user discounts")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error deleting user: {str(e)}")) 