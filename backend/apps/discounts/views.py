# apps/discounts/views.py

from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from apps.shopware.client import ShopwareClient
from apps.shopware.models import ShopwareCredential

@staff_member_required
def get_shopware_values(request, condition_type):
    try:
        credential = ShopwareCredential.objects.filter(is_active=True).first()
        if not credential:
            return JsonResponse({'error': 'Geen actieve Shopware credentials gevonden'}, status=400)

        client = ShopwareClient(credential)

        if condition_type == 'manufacturer':
            endpoint = 'search/product-manufacturer'
        elif condition_type == 'category':
            endpoint = 'search/category'
        elif condition_type == 'tag':
            endpoint = 'search/tag'
        else:
            return JsonResponse({'error': 'Ongeldig condition type'}, status=400)

        response = client.make_request('POST', endpoint)
        values = [{'id': item['id'], 'name': item['name']}
                 for item in response.get('data', [])]

        return JsonResponse(values, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
