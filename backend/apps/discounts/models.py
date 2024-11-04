# apps/discounts/models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class DiscountRule(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    # Timing
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    # Discount configuration
    discount_type = models.CharField(
        max_length=20,
        choices=[
            ('percentage', 'Percentage'),
            ('fixed', 'Fixed Amount')
        ]
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    # Priority for overlapping rules
    priority = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return self.name

class DiscountCondition(models.Model):
    discount_rule = models.ForeignKey(
        DiscountRule,
        on_delete=models.CASCADE,
        related_name='conditions'
    )

    condition_type = models.CharField(
        max_length=20,
        choices=[
            ('manufacturer', 'Manufacturer'),
            ('category', 'Category'),
            ('tag', 'Tag'),
            ('property', 'Property'),
            ('price', 'Price Range')
        ]
    )

    # For storing condition values (e.g., category IDs, price ranges, etc.)
    value = models.JSONField()

    # Logical operators for combining conditions
    operator = models.CharField(
        max_length=3,
        choices=[
            ('AND', 'AND'),
            ('OR', 'OR')
        ],
        default='AND'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.condition_type} condition for {self.discount_rule.name}"
