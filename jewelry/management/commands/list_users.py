from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "List all users and their status"

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            type=str,
            help="Filter by email (partial match)",
        )
        parser.add_argument(
            "--active-only",
            action="store_true",
            help="Show only active users",
        )
        parser.add_argument(
            "--inactive-only",
            action="store_true",
            help="Show only inactive users",
        )

    def handle(self, *args, **options):
        email_filter = options.get("email", "")
        active_only = options.get("active_only", False)
        inactive_only = options.get("inactive_only", False)

        users = User.objects.all()
        
        if email_filter:
            users = users.filter(email__icontains=email_filter)
        
        if active_only:
            users = users.filter(is_active=True)
        
        if inactive_only:
            users = users.filter(is_active=False)

        if not users.exists():
            self.stdout.write("No users found.")
            return

        self.stdout.write(f"Found {users.count()} user(s):")
        self.stdout.write("-" * 100)
        self.stdout.write(f"{'ID':<5} {'Email':<35} {'Username':<25} {'Active':<8} {'Staff':<8} {'Date Joined'}")
        self.stdout.write("-" * 100)

        for user in users:
            self.stdout.write(
                f"{user.id:<5} {user.email:<35} {user.username:<25} {str(user.is_active):<8} {str(user.is_staff):<8} {user.date_joined.strftime('%Y-%m-%d %H:%M')}"
            )
        
        # Summary
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        inactive_users = User.objects.filter(is_active=False).count()
        
        self.stdout.write("-" * 100)
        self.stdout.write(f"Summary: Total={total_users}, Active={active_users}, Inactive={inactive_users}") 