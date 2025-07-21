
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jewelry", "0026_add_hover_image_field"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="completed_at",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Completed At"
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="currency",
            field=models.CharField(
                choices=[
                    ("INR", "Indian Rupee (INR)"),
                    ("USD", "US Dollar (USD)"),
                    ("EUR", "Euro (EUR)"),
                    ("GBP", "British Pound (GBP)"),
                    ("CAD", "Canadian Dollar (CAD)"),
                    ("AUD", "Australian Dollar (AUD)"),
                    ("SGD", "Singapore Dollar (SGD)"),
                    ("AED", "UAE Dirham (AED)"),
                ],
                default="INR",
                max_length=3,
                verbose_name="Currency",
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="description",
            field=models.CharField(
                default="Custom Payment",
                max_length=255,
                verbose_name="Payment Description",
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="notes",
            field=models.TextField(blank=True, verbose_name="Additional Notes"),
        ),
        migrations.AddField(
            model_name="payment",
            name="platform",
            field=models.CharField(
                choices=[("razorpay", "Razorpay")],
                default="razorpay",
                max_length=20,
                verbose_name="Payment Platform",
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="razorpay_payment_id",
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                verbose_name="Razorpay Payment ID",
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="amount",
            field=models.DecimalField(
                decimal_places=2, max_digits=10, verbose_name="Amount Paid"
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="status",
            field=models.CharField(
                choices=[
                    ("created", "Created"),
                    ("pending", "Pending"),
                    ("completed", "Completed"),
                    ("failed", "Failed"),
                    ("cancelled", "Cancelled"),
                    ("refunded", "Refunded"),
                ],
                default="created",
                max_length=20,
                verbose_name="Payment Status",
            ),
        ),
    ]
