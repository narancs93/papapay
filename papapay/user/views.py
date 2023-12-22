from django.contrib.auth import get_user_model, login, logout
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
        user = request.user
        profile_serializer = UserProfileSerializer(data={
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
        if not profile_serializer.is_valid():
            profile_serializer = UserProfileSerializer()
        return Response({
            'profile_serializer': profile_serializer,
            'password_update_serializer': PasswordUpdateSerializer(),
            'style': self.style
        })
