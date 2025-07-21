
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jewelry", "0020_userdiscount"),
    ]

    operations = [
        migrations.CreateModel(
            name="DiamondProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Diamond Name")),
                ("description", models.TextField(verbose_name="Description")),
                (
                    "image",
                    models.ImageField(
                        upload_to="product_images/", verbose_name="Diamond Image"
                    ),
                ),
                (
                    "carat",
                    models.DecimalField(
                        decimal_places=3, max_digits=6, verbose_name="Carat Weight"
                    ),
                ),
                (
                    "shape",
                    models.CharField(
                        help_text="e.g., Round, Princess, Emerald, etc.",
                        max_length=50,
                        verbose_name="Shape",
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        help_text="e.g., D, E, F, G, etc.",
                        max_length=10,
                        verbose_name="Color Grade",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("available", "Available"),
                            ("sold", "Sold"),
                            ("reserved", "Reserved"),
                            ("inactive", "Inactive"),
                        ],
                        default="available",
                        max_length=20,
                        verbose_name="Status",
                    ),
                ),
                (
                    "badge",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("premium", "Premium"),
                            ("best_seller", "Best Seller"),
                            ("new", "New"),
                            ("exclusive", "Exclusive"),
                            ("limited", "Limited"),
                        ],
                        max_length=20,
                        null=True,
                        verbose_name="Badge",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
            ],
            options={
                "verbose_name": "Diamond Product",
                "verbose_name_plural": "Diamond Products",
                "ordering": ["-created_at"],
            },
        ),
    ]
