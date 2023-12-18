from django.db import models
from papapay.postal_address.models import Country
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class PhoneNumber(models.Model):
    name = models.CharField(max_length=64)
    country = models.ForeignKey(Country, related_name='phone_numbers', on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=20)
    owner_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    owner_id = models.PositiveIntegerField()
    owner = GenericForeignKey("owner_type", "owner_id")

    def __str__(self):
        return f'{self.name} (id={self.id})'

    class Meta:
        indexes = [
            models.Index(fields=["owner_id", "owner_id"]),
        ]
        unique_together = ('country', 'phone_number')
