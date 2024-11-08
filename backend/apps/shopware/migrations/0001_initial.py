# Generated by Django 4.2.16 on 2024-11-04 19:54

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ShopwareCredential",
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
                    "name",
                    models.CharField(
                        help_text="Naam voor deze API configuratie", max_length=255
                    ),
                ),
                ("api_url", models.URLField(help_text="Shopware API base URL")),
                ("client_id", models.CharField(max_length=255)),
                ("client_secret", models.CharField(max_length=255)),
                (
                    "access_token",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("token_expires_at", models.DateTimeField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Shopware Credential",
                "verbose_name_plural": "Shopware Credentials",
            },
        ),
    ]
