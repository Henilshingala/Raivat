# Generated by Django 5.2.4 on 2025-07-05 18:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jewelry", "0016_userprofile_delete_customuser"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="OTP",
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
                (
                    "email",
                    models.EmailField(max_length=254, verbose_name="Email Address"),
                ),
                ("otp_code", models.CharField(max_length=6, verbose_name="OTP Code")),
                (
                    "otp_type",
                    models.CharField(
                        choices=[
                            ("email_verification", "Email Verification"),
                            ("login", "Login"),
                            ("password_reset", "Password Reset"),
                        ],
                        max_length=20,
                        verbose_name="OTP Type",
                    ),
                ),
                ("is_used", models.BooleanField(default=False, verbose_name="Is Used")),
                ("expires_at", models.DateTimeField(verbose_name="Expires At")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="otps",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "OTP",
                "verbose_name_plural": "OTPs",
                "ordering": ["-created_at"],
            },
        ),
    ]
