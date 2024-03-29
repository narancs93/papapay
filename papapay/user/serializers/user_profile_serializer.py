from django.contrib.auth import get_user_model
from rest_framework import serializers

from ...common.models import PhoneNumber

User = get_user_model()


class PhoneNumberChoice:
    def __init__(self, phone_number_obj):
        self.phone_number = repr(phone_number_obj)
        self.id = phone_number_obj.id
        self.name = phone_number_obj.name
        self.alpha2_code = phone_number_obj.country.alpha2_code
        self.number = phone_number_obj.phone_number

    def __str__(self):
        return self.phone_number


class PhoneNumbersChoiceField(serializers.MultipleChoiceField):

    def to_internal_value(self, data, *args, **kwargs):
        data = list(map(lambda x: int(x), data))
        phone_number_id_choices = (choice.id for choice in self.choices)
        phone_numbers = set()

        for phone_number_id in data:
            if phone_number_id in phone_number_id_choices:
                phone_numbers.add(PhoneNumber.objects.get(pk=phone_number_id))
            else:
                pass

        return phone_numbers


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    phone_numbers = PhoneNumbersChoiceField(
        choices=[], required=False, allow_null=True, allow_blank=True,
        style={
            'base_template': 'phone_numbers.html',
            'no_items_message': 'You do not have any phone numbers configured yet.'
        })

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_numbers')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            user = User.objects.get(email=self.initial_data.get('email'))
            self.fields['phone_numbers'].choices = [
                PhoneNumberChoice(phone_number) for phone_number
                in PhoneNumber.objects.filter(owner_person=user)
            ]
        except User.DoesNotExist:
            self.fields['phone_numbers'].choices = []

    def validate(self, data):
        self.validate_inputs_are_not_empty(data)

        return data

    def validate_inputs_are_not_empty(self, data):
        error_message_for_fields = {
            'email': 'Email address is required. Please enter a valid email.',
            'first_name': 'First name is required.',
            'last_name': 'Last name is required.',
        }
        validation_errors = {}

        for field, error_message in error_message_for_fields.items():
            if not data.get(field):
                validation_errors[field] = error_message

        if validation_errors:
            raise serializers.ValidationError(validation_errors)
