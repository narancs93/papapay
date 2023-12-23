from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_null=True, allow_blank=True,)
    last_name = serializers.CharField(required=False, allow_null=True, allow_blank=True,)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

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
