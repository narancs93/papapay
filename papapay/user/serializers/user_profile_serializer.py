from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from papapay.common.models import PhoneNumber

User = get_user_model()
USER_CONTENT_TYPE = ContentType.objects.get(app_label='user', model='user')


class PhoneNumberChoice:
    def __init__(self, phone_number, id):
        self.phone_number = phone_number
        self.id = id

    def __str__(self):
        return self.phone_number


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    phone_numbers = serializers.ChoiceField(
        choices=[], required=False, allow_null=True, allow_blank=True,
        style={
            'base_template': 'select_multiple.html',
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
                PhoneNumberChoice(repr(phone_number), phone_number.id) for phone_number
                in PhoneNumber.objects.filter(owner_id=user.id, owner_type=USER_CONTENT_TYPE)
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
