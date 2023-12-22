from django.contrib.auth import authenticate, get_user_model
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


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class PasswordUpdateSerializer(serializers.Serializer):
    password = serializers.CharField(label='Current password')
    new_password = serializers.CharField(label='New password')
    new_password2 = serializers.CharField(label='Confirm new password')

    class Meta:
        fields = ('password', 'new_password', 'new_password2')
