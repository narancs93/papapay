from django.contrib.auth import (get_user_model, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (LoginSerializer, PasswordUpdateSerializer,
                          SignupSerializer, UserProfileSerializer)
from ..common.models import PhoneNumber
from ..common.serializers import PhoneNumberSerializer

User = get_user_model()


class SignupView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/signup.html'
    style = {'template_pack': 'user/serializers/horizontal'}

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('papapay.home:home-url'))
        serializer = SignupSerializer()
        return Response({'serializer': serializer, 'style': self.style})

    def post(self, request):
        serializer = SignupSerializer(data=request.POST)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'style': self.style})
        serializer.save()
        return redirect('papapay.user:login')


class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/login.html'
    style = {'template_pack': 'user/serializers/horizontal'}

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('papapay.home:home-url'))
        serializer = LoginSerializer()
        return Response({'serializer': serializer, 'style': self.style})

    def post(self, request):
        serializer = LoginSerializer(data=request.POST, context={'request': request})

        if serializer.is_valid():
            user = serializer.get_authenticated_user()
            login(request, user)
            return redirect('papapay.home:home-url')

        else:
            return Response({'serializer': serializer, 'style': self.style})


class LogoutView(APIView):

    def get(self, request):
        logout(request)
        return redirect('papapay.home:home-url')


class ProfileView(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/profile.html'
    style = {'template_pack': 'user/serializers/horizontal'}

    def get(self, request):
        return Response({
            'profile_serializer': self.get_profile_serializer(request.user),
            'password_update_serializer': PasswordUpdateSerializer(),
            'add_phone_number_serializer': PhoneNumberSerializer(),
            'update_phone_number_serializer': PhoneNumberSerializer(),
            'remove_phone_number_from_profile_api': reverse('papapay.user:remove-phone-number-from-profile-api'),
            'style': self.style
        })

    def post(self, request):
        update_type = request.data.get('_update_type')

        self.initialize_serializers(request)
        self.initialize_flags()
        self.perform_update(update_type)

        response_data = {
            'profile_serializer':
                self.profile_serializer if update_type == 'profile' else self.get_profile_serializer(request.user),
            'profile_was_updated':
                self.profile_updated,
            'password_update_serializer':
                self.password_update_serializer if update_type == 'password' else PasswordUpdateSerializer(),
            'password_was_updated':
                self.password_updated,
            'add_phone_number_serializer':
                self.add_phone_number_serializer if update_type == 'add_phone_number' else PhoneNumberSerializer(),
            'update_phone_number_serializer':
                self.update_phone_number_serializer if
                update_type == 'update_phone_number' else PhoneNumberSerializer(),
            'style': self.style
        }
        return Response(response_data)

    def get_profile_serializer(self, user):
        profile_serializer = UserProfileSerializer(data={
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
        profile_serializer.is_valid()
        return profile_serializer

    def initialize_serializers(self, request):
        self.profile_serializer = UserProfileSerializer(instance=request.user, data=request.data)
        self.password_update_serializer = PasswordUpdateSerializer(instance=request.user, data=request.data)
        self.add_phone_number_serializer = PhoneNumberSerializer(
            owner=request.user, alpha2_code=request.data.get('alpha2_code'), data=request.data)

        phone_number_id = request.data.get('phone_number_id')
        if phone_number_id:
            phone_number = PhoneNumber.objects.get(id=phone_number_id)
            self.update_phone_number_serializer = PhoneNumberSerializer(
                instance=phone_number,
                owner=request.user,
                alpha2_code=request.data.get('alpha2_code'),
                data=request.data
            )

    def initialize_flags(self):
        self.profile_updated = False
        self.password_updated = False

    def perform_update(self, update_type):
        if update_type == 'profile' and self.profile_serializer.is_valid():
            self.profile_serializer.save()
            self.profile_updated = True
        elif update_type == 'password' and self.password_update_serializer.is_valid():
            self.password_update_serializer.save()
            self.password_updated = True
            update_session_auth_hash(self.request, self.request.user)
        elif update_type == 'add_phone_number' and self.add_phone_number_serializer.is_valid():
            self.add_phone_number_serializer.save()
        elif update_type == 'update_phone_number' and self.update_phone_number_serializer.is_valid():
            self.update_phone_number_serializer.save()


class RemovePhoneNumberFromUser(APIView):

    def post(self, request):
        phone_number_id = request.data.get('phone_number_id')

        if phone_number_id:
            phone_number = PhoneNumber.objects.filter(id=phone_number_id)
            if phone_number.exists() and phone_number[0].owner_person == request.user:
                phone_number[0].delete()
                return Response('Phone number deleted successfully.', status=status.HTTP_200_OK)

        return Response('Invalid request', status=status.HTTP_400_BAD_REQUEST)
