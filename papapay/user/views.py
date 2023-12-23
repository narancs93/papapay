from django.contrib.auth import (get_user_model, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (LoginSerializer, PasswordUpdateSerializer,
                          SignupSerializer, UserProfileSerializer)

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
            'style': self.style
        })

    def post(self, request):
        profile_serializer, password_update_serializer = None, None
        self.profile_was_updated, self.password_was_updated = False, False

        update_type = request.POST.get('_update_type')
        if update_type == 'profile':
            profile_serializer = self.update_profile(request)
        elif update_type == 'password':
            password_update_serializer = self.update_password(request)

        return Response({
            'profile_serializer': profile_serializer or self.get_profile_serializer(request.user),
            'profile_was_updated': self.profile_was_updated,
            'password_update_serializer': password_update_serializer or PasswordUpdateSerializer(),
            'password_was_updated': self.password_was_updated,
            'style': self.style
        })

    def get_profile_serializer(self, user):
        profile_serializer = UserProfileSerializer(data={
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
        if profile_serializer.is_valid():
            return profile_serializer
        return UserProfileSerializer()

    def update_profile(self, request):
        serializer = UserProfileSerializer(instance=request.user, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            self.profile_was_updated = True
        return serializer

    def update_password(self, request):
        serializer = PasswordUpdateSerializer(instance=request.user, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            update_session_auth_hash(request, request.user)
            self.password_was_updated = True
        return serializer
