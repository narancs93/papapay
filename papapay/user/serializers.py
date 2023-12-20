from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(
        write_only=True, required=True, label='Confirm password', style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password2', )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'],
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
            raise serializers.ValidationError({'password': 'Invalid username or password'})
        return data

    def validate_email_and_password_not_empty(self, data):
        validation_errors = {}

        if not data.get('email'):
            validation_errors['email'] = 'Email address is required. Please enter a valid email.'
        if not data.get('password'):
            validation_errors['password'] = 'Password is required.'

        if validation_errors:
            raise serializers.ValidationError(validation_errors)
