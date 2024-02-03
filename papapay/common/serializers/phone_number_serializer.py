from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import PhoneNumber
from ..utils import remove_prefix
from ...postal_address.models import Country
from ...restaurant.models import Restaurant

User = get_user_model()


class PhoneNumberSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone_number = serializers.CharField()

    def __init__(self, *args, owner=None, alpha2_code=None, **kwargs):
        self.owner = owner
        if isinstance(owner, User):
            self.owner_type = 'owner_person'
        elif isinstance(owner, Restaurant):
            self.owner_type = 'owner_restaurant'
        elif owner:
            raise ValueError('PhoneNumber.owner must be a User or a Restaurant')

        self.alpha2_code = alpha2_code
        super().__init__(*args, **kwargs)

    def create(self, *args, **kwargs):
        if not self.alpha2_code and not isinstance(self.alpha2_code, str):
            raise ValueError('alpha2_code must be specified')
        country = Country.objects.get(alpha2_code=self.alpha2_code.upper())

        owner_kwargs = {self.owner_type: self.owner}
        phone_number = PhoneNumber.objects.create(
            name=args[0]['name'],
            country=country,
            phone_number=remove_prefix(args[0]['phone_number'], country.international_call_prefix),
            **owner_kwargs
        )
        return phone_number

    def update(self, instance, validated_data):
        country = Country.objects.get(alpha2_code=self.alpha2_code.upper())
        instance.name = validated_data['name']
        instance.country = country
        instance.phone_number = remove_prefix(validated_data['phone_number'], country.international_call_prefix)
        instance.save()

        return instance
