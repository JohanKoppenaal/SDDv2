from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class DiscountRule(models.Model):
    """Hoofdmodel voor kortingsregels"""
    name = models.CharField(
        max_length=255,
        verbose_name="Naam",
        help_text="Naam van de kortingsregel"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Beschrijving",
        help_text="Optionele beschrijving van de kortingsregel"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Actief",
        help_text="Is deze kortingsregel momenteel actief?"
    )

    # Timing
    start_date = models.DateTimeField(
        verbose_name="Startdatum",
        help_text="Wanneer gaat de korting in?"
    )
    end_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Einddatum",
        help_text="Wanneer eindigt de korting? Leeg = geen einddatum"
    )

    # Korting configuratie
    discount_type = models.CharField(
        max_length=20,
        choices=[
            ('percentage', 'Percentage'),
            ('fixed', 'Vast bedrag')
        ],
        verbose_name="Type korting"
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Kortingswaarde",
        help_text="Percentage of vast bedrag van de korting"
    )

    # Prioriteit voor overlappende regels
    priority = models.IntegerField(
        default=0,
        verbose_name="Prioriteit",
        help_text="Hogere waarde = hogere prioriteit bij overlappende regels"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kortingsregel"
        verbose_name_plural = "Kortingsregels"
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return self.name

class DiscountCondition(models.Model):
    """Model voor de voorwaarden van een kortingsregel"""
    discount_rule = models.ForeignKey(
        DiscountRule,
        on_delete=models.CASCADE,
        related_name='conditions',
        verbose_name="Kortingsregel"
    )

    condition_type = models.CharField(
        max_length=20,
        choices=[
            ('manufacturer', 'Fabrikant'),
            ('category', 'Categorie'),
            ('tag', 'Tag'),
            ('property', 'Eigenschap'),
            ('price', 'Prijsbereik')
        ],
        verbose_name="Type voorwaarde"
    )

    # Voor het opslaan van voorwaarde waarden (bijv. category IDs, prijsbereiken)
    value = models.JSONField(
        verbose_name="Waarde",
        help_text="JSON waarde voor de voorwaarde"
    )

    operator = models.CharField(
        max_length=3,
        choices=[
            ('AND', 'EN'),
            ('OR', 'OF')
        ],
        default='AND',
        verbose_name="Operator"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kortingsvoorwaarde"
        verbose_name_plural = "Kortingsvoorwaarden"

    def __str__(self):
        return f"{self.get_condition_type_display()} voorwaarde voor {self.discount_rule.name}"
