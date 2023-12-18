from django.db import models
from papapay.postal_address.models import Country
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class PhoneNumber(models.Model):
    name = models.CharField(max_length=64)
    country = models.ForeignKey(Country, related_name='phone_numbers', on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=20)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    owner = GenericForeignKey("content_type", "object_id")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} (id={self.id})'

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        unique_together = ('country', 'phone_number')
