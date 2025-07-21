from django.core.management.base import BaseCommand
from jewelry.models import ProductCategory


class Command(BaseCommand):
    help = "Update categories by removing old ones and adding new ones"

    def handle(self, *args, **options):
        # Delete old categories that are no longer in choices
        old_categories = ["modern", "luxury", "budget"]
        for category_name in old_categories:
            try:
                category = ProductCategory.objects.get(name=category_name)
                category.delete()
                self.stdout.write(f"Deleted category: {category_name}")
            except ProductCategory.DoesNotExist:
                self.stdout.write(f"Category {category_name} not found")

        # Create new 'other' category if it doesn't exist
        try:
            other_category = ProductCategory.objects.get(name="other")
            self.stdout.write("Category 'other' already exists")
        except ProductCategory.DoesNotExist:
            other_category = ProductCategory.objects.create(
                name="other",
                display_name="Other",
                description="Special and unique jewelry items",
                icon="star",
                sort_order=25,
                is_active=True,
            )
            self.stdout.write("Created category: Other")

        self.stdout.write(self.style.SUCCESS("Category update completed!"))
