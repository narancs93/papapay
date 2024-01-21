from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class PasswordUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=False, write_only=True, allow_null=True, allow_blank=True,
        label='Current password', style={'input_type': 'password'})
    new_password = serializers.CharField(
        required=False, write_only=True, allow_null=True, allow_blank=True,
        validators=[validate_password], style={'input_type': 'password'})
    new_password2 = serializers.CharField(
        required=False, write_only=True, allow_null=True, allow_blank=True,
        label='Confirm new password', style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('password', 'new_password', 'new_password2')

    def validate(self, data):
        self.validate_current_password_is_correct(data)
        self.validate_new_passwords_match(data)

        return data

    def validate_current_password_is_correct(self, data):
        if not self.instance.check_password(data['password']):
            raise serializers.ValidationError({'password': 'Current password does not match.'})

    def validate_new_passwords_match(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})

    def update(self, instance, *args, **kwargs):
        user = super().update(instance, *args, **kwargs)
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
