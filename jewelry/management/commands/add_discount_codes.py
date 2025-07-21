import random

from django.core.management.base import BaseCommand
from jewelry.models import DiscountCode


class Command(BaseCommand):
    help = "Add sample discount codes for testing"

    def handle(self, *args, **options):
        # Sample discount codes with different percentages
        discount_data = [
            {"code": "WELCOME10", "percentage": 10},
            {"code": "NEWUSER15", "percentage": 15},
            {"code": "SPECIAL20", "percentage": 20},
            {"code": "VIP25", "percentage": 25},
            {"code": "PREMIUM30", "percentage": 30},
            {"code": "EXCLUSIVE35", "percentage": 35},
            {"code": "ELITE40", "percentage": 40},
            {"code": "ROYAL45", "percentage": 45},
            {"code": "DIAMOND50", "percentage": 50},
        ]

        created_count = 0
        for data in discount_data:
            code, created = DiscountCode.objects.get_or_create(
                code=data["code"], defaults={"percentage": data["percentage"]}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created discount code: {code.code} - {code.percentage}%"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Discount code already exists: {code.code} - {code.percentage}%"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully processed {len(discount_data)} discount codes. {created_count} new codes created."
            )
        )
