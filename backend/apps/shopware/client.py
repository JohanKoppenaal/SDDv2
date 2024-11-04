# apps/shopware/client.py

import requests
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from .models import ShopwareCredential

class ShopwareClient:
    def __init__(self, credential: ShopwareCredential):
        self.credential = credential
        self.base_url = credential.api_url.rstrip('/')
        self.session = requests.Session()

    def get_access_token(self):
        """Verkrijg of vernieuw het access token."""
        if self._is_token_valid():
            return self.credential.access_token

        url = f"{self.base_url}/api/oauth/token"
        data = {
            'client_id': self.credential.client_id,
            'client_secret': self.credential.client_secret,
            'grant_type': 'client_credentials'
        }

        response = requests.post(url, data=data)
        response.raise_for_status()

        token_data = response.json()
        self.credential.access_token = token_data['access_token']
        # Gebruik timezone.now() in plaats van datetime.now()
        self.credential.token_expires_at = timezone.now() + timedelta(seconds=token_data['expires_in'])
        self.credential.save()

        return self.credential.access_token

    def _is_token_valid(self):
        """Check of het huidige token nog geldig is."""
        if not self.credential.access_token or not self.credential.token_expires_at:
            return False

        # Gebruik timezone.now() in plaats van datetime.now()
        return timezone.now() < self.credential.token_expires_at - timedelta(minutes=5)

    def make_request(self, method, endpoint, **kwargs):
        """Maak een API request met automatische token vernieuwing."""
        url = f"{self.base_url}/api/{endpoint.lstrip('/')}"
        headers = {
            'Authorization': f'Bearer {self.get_access_token()}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            **kwargs
        )
        response.raise_for_status()
        return response.json()

    def test_connection(self):
        """Test de API verbinding."""
        try:
            return self.make_request('GET', '_info/version')
        except Exception as e:
            return False, str(e)
