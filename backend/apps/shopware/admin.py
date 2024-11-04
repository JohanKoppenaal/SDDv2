# apps/shopware/admin.py

from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.safestring import mark_safe
from .models import ShopwareCredential
from .client import ShopwareClient

@admin.register(ShopwareCredential)
class ShopwareCredentialAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_url', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'api_url')
    readonly_fields = ('access_token', 'token_expires_at', 'created_at', 'updated_at', 'test_connection_button')

    def test_connection_button(self, obj):
        if obj.id:
            return mark_safe(f'''
                <button type="button" onclick="testConnection({obj.id})" class="button">
                    Test Verbinding
                </button>
                <span id="test-result-{obj.id}"></span>
                <script>
                    function testConnection(id) {{
                        fetch('/admin/shopware/shopwarecredential/' + id + '/test-connection/')
                            .then(response => response.json())
                            .then(data => {{
                                const resultSpan = document.getElementById('test-result-' + id);
                                resultSpan.innerHTML = data.success ?
                                    '<span style="color: green; margin-left: 10px;">✓ Verbinding succesvol!</span>' :
                                    '<span style="color: red; margin-left: 10px;">✗ ' + data.error + '</span>';
                            }});
                    }}
                </script>
            ''')
        return "Sla eerst de credentials op om te testen"
    test_connection_button.short_description = "Test Verbinding"
    test_connection_button.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:credential_id>/test-connection/',
                self.admin_site.admin_view(self.test_connection_view),
                name='shopware-credential-test',
            ),
        ]
        return custom_urls + urls

    def test_connection_view(self, request, credential_id):
        try:
            credential = ShopwareCredential.objects.get(id=credential_id)
            client = ShopwareClient(credential)
            response = client.make_request('GET', '_info/version')
            return JsonResponse({
                'success': True,
                'version': response.get('version', 'Onbekend')
            })
        except ShopwareCredential.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Credentials niet gevonden'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
