from django.contrib.auth.models import Permission
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from papapay.postal_address.models import Country


class PhoneNumber(models.Model):
    name = models.CharField(max_length=64)
    country = models.ForeignKey(Country, related_name='phone_numbers', on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=20)
    owner_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    owner_id = models.PositiveIntegerField()
    owner = GenericForeignKey("owner_type", "owner_id")

    def get_international_call_prefix(self):
        return f'{self.country.international_call_prefix} ' if self.country and \
            self.country.international_call_prefix else ''

    def __str__(self):
        return f'{self.get_international_call_prefix()}{self.phone_number} (id={self.id})'

    def __repr__(self):
        return f'{self.name} ({self.get_international_call_prefix()}{self.phone_number})'

    class Meta:
        indexes = [
            models.Index(fields=["owner_id", "owner_id"]),
        ]
        unique_together = ('country', 'phone_number')


class PageAccess(models.Model):
    app_name = models.CharField(max_length=150)
    url_name = models.CharField(max_length=150)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return f'{self.app_name}.{self.url_name} (id={self.id})'

    class Meta:
        verbose_name_plural = 'Page accesses'
