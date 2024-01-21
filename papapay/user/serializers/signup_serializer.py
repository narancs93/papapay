from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=False, allow_null=True, allow_blank=True,
            validators=[UniqueValidator(queryset=User.objects.all(), message='This email address is already in use.')]
            )

    password = serializers.CharField(
        required=False, write_only=True, allow_null=True, allow_blank=True,
        validators=[validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(
        required=False, write_only=True, allow_null=True, allow_blank=True,
        label='Confirm password', style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password2', )
        extra_kwargs = {
            'first_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'last_name': {'required': False, 'allow_null': True, 'allow_blank': True},
        }

    def validate(self, data):
        self.validate_inputs_are_not_empty(data)
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return data

    def validate_inputs_are_not_empty(self, data):
        error_message_for_fields = {
            'first_name': 'First name is required.',
            'last_name': 'Last name is required.',
            'email': 'Email address is required. Please enter a valid email.',
            'password': 'Password is required.',
            'password2': 'Confirm password is required.'
        }
        validation_errors = {}

        for field, error_message in error_message_for_fields.items():
            if not data.get(field):
                validation_errors[field] = error_message

        if validation_errors:
            raise serializers.ValidationError(validation_errors)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
