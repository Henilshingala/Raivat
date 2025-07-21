import random
import string

from django.core.management.base import BaseCommand
from jewelry.models import DiscountCode


class Command(BaseCommand):
    help = "Generate 10 discount codes with percentages from 1% to 10%"

    def handle(self, *args, **options):
        # Clear existing discount codes
        DiscountCode.objects.all().delete()
        self.stdout.write("Cleared existing discount codes...")

        # Generate 10 codes with percentages 1% to 10%
        for percentage in range(1, 11):
            # Generate a unique 6-character code
            while True:
                code = "".join(
                    random.choices(string.ascii_uppercase + string.digits, k=6)
                )
                if not DiscountCode.objects.filter(code=code).exists():
                    break

            # Create the discount code
            DiscountCode.objects.create(code=code, percentage=percentage)
            self.stdout.write(f"Created code: {code} - {percentage}%")

        self.stdout.write(
            self.style.SUCCESS("Successfully generated 10 discount codes!")
        )
