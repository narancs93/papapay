from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from papapay.common.models import PhoneNumber
from papapay.common.utils import remove_prefix
from papapay.postal_address.models import Country

USER_CONTENT_TYPE = ContentType.objects.get(app_label='user', model='user')


class AddPhoneNumberSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone_number = serializers.CharField()

    def __init__(self, *args, user=None, alpha2_code=None, **kwargs):
        self.user = user
        self.alpha2_code = alpha2_code
        super().__init__(*args, **kwargs)

    def create(self, *args, **kwargs):
        if not self.alpha2_code and not isinstance(self.alpha2_code, str):
            raise ValueError('alpha2_code must be specified')
        country = Country.objects.get(alpha2_code=self.alpha2_code.upper())
        phone_number = PhoneNumber.objects.create(
            name=args[0]['name'],
            country=country,
            phone_number=remove_prefix(args[0]['phone_number'], country.international_call_prefix),
            owner_id=self.user.id,
            owner_type=USER_CONTENT_TYPE
        )
        return phone_number

    def update(self, instance, validated_data):
        country = Country.objects.get(alpha2_code=self.alpha2_code.upper())
        instance.name = validated_data['name']
        instance.country = country
        instance.phone_number = remove_prefix(validated_data['phone_number'], country.international_call_prefix)
        instance.save()

        return instance
