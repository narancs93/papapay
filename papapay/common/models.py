from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.db import models

from ..postal_address.models import Country
from ..restaurant.models import Restaurant

User = get_user_model()


class PhoneNumber(models.Model):
    name = models.CharField(max_length=64)
    country = models.ForeignKey(Country, related_name='phone_numbers', on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=20)
    owner_person = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    owner_restaurant = models.ForeignKey(Restaurant, null=True, blank=True, on_delete=models.PROTECT)

    @property
    def owner(self):
        if self.owner_person_id is not None:
            return self.owner_person
        elif self.owner_restaurant_id is not None:
            return self.owner_restaurant
        raise AssertionError("Neither 'owner_person' nor 'owner_restaurant' is set.")

    def clean(self):
        if self.owner_person and self.owner_restaurant:
            raise ValidationError('A PhoneNumber cannot be associated with both a User and a Restaurant.')

    def get_international_call_prefix(self):
        return f'{self.country.international_call_prefix} ' if self.country and \
            self.country.international_call_prefix else ''

    def __str__(self):
        return f'{self.get_international_call_prefix()}{self.phone_number} (id={self.id})'

    def __repr__(self):
        return f'{self.name} ({self.get_international_call_prefix()}{self.phone_number})'

    class Meta:
        unique_together = ('country', 'phone_number')


class PageAccess(models.Model):
    app_name = models.CharField(max_length=150)
    url_name = models.CharField(max_length=150)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return f'{self.app_name}.{self.url_name} (id={self.id})'

    class Meta:
        verbose_name_plural = 'Page accesses'
