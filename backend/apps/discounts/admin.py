# apps/discounts/admin.py

from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import DiscountRule, DiscountCondition
from apps.shopware.client import ShopwareClient
from apps.shopware.models import ShopwareCredential

class DiscountConditionForm(forms.ModelForm):
    shopware_value = forms.ChoiceField(
        required=False,
        label="Selecteer waarde",
        help_text="Selecteer een waarde uit Shopware"
    )

    class Meta:
        model = DiscountCondition
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initieel lege keuzes
        self.fields['shopware_value'].choices = [('', '-----')]

        # Als we een bestaande instance hebben
        if self.instance and self.instance.pk:
            try:
                credential = ShopwareCredential.objects.filter(is_active=True).first()
                if credential:
                    client = ShopwareClient(credential)

                    # Haal keuzes op gebaseerd op condition_type
                    if self.instance.condition_type == 'manufacturer':
                        response = client.make_request('POST', 'search/product-manufacturer')
                        print(f"Manufacturer response: {response}")  # Debug print
                        choices = [(str(item['id']), item['name'])
                                 for item in response.get('data', [])]
                        self.fields['shopware_value'].choices = [('', '-----')] + choices
                    elif self.instance.condition_type == 'category':
                        response = client.make_request('POST', 'search/category')
                        print(f"Category response: {response}")  # Debug print
                        choices = [(str(item['id']), item['name'])
                                 for item in response.get('data', [])]
                    elif self.instance.condition_type == 'tag':
                        response = client.make_request('POST', 'search/tag')
                        print(f"tag response: {response}")  # Debug print
                        choices = [(str(item['id']), item['name'])
                                 for item in response.get('data', [])]

                    self.fields['shopware_value'].choices = [('', '-----')] + choices
            except Exception as e:
                self.fields['shopware_value'].help_text = f"Fout bij ophalen Shopware data: {str(e)}"

    def clean(self):
        cleaned_data = super().clean()
        # Zet de geselecteerde waarde om naar het juiste JSON formaat
        if cleaned_data.get('shopware_value'):
            cleaned_data['value'] = {
                'id': cleaned_data['shopware_value'],
                'type': cleaned_data.get('condition_type')
            }
        return cleaned_data

class DiscountConditionInline(admin.TabularInline):
    model = DiscountCondition
    form = DiscountConditionForm
    extra = 1
    fields = ('condition_type', 'shopware_value', 'operator')

@admin.register(DiscountRule)
class DiscountRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_type', 'discount_value', 'is_active', 'start_date', 'end_date')
    list_filter = ('is_active', 'discount_type', 'start_date')
    search_fields = ('name', 'description')
    inlines = [DiscountConditionInline]
    ordering = ('-priority', '-created_at')

    class Media:
        js = ('admin/js/discount_conditions.js',)
