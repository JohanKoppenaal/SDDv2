# apps/shopware/models.py

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from cryptography.fernet import Fernet

class ShopwareCredential(models.Model):
    name = models.CharField(max_length=255, help_text="Naam voor deze API configuratie")
    api_url = models.URLField(help_text="Shopware API base URL")
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255, blank=True, null=True)
    token_expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Shopware Credential"
        verbose_name_plural = "Shopware Credentials"

    def __str__(self):
        return f"{self.name} ({self.api_url})"

    def save(self, *args, **kwargs):
        # Hier kunnen we encryptie toevoegen voor client_secret
        super().save(*args, **kwargs)
