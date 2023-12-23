from django.contrib.auth import authenticate, get_user_model

from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=False)
    password = serializers.CharField(
        required=False,
        label=("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def get_authenticated_user(self):
        return self.user

    def validate(self, data):
        self.validate_email_and_password_not_empty(data)
        self.user = authenticate(
            request=self.context.get('request'), email=data.get('email'), password=data.get('password'))
        if self.user is None:
            raise serializers.ValidationError({'password': 'Invalid email or password.'})
        return data

    def validate_email_and_password_not_empty(self, data):
        validation_errors = {}

        if not data.get('email'):
            validation_errors['email'] = 'Email address is required. Please enter a valid email.'
        if not data.get('password'):
            validation_errors['password'] = 'Password is required.'

        if validation_errors:
            raise serializers.ValidationError(validation_errors)
