from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegisterSerializer

User = get_user_model()


class SignupView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/signup.html'
    style = {'template_pack': 'user/serializers/horizontal'}

    def get(self, request):
        serializer = RegisterSerializer()
        return Response({'serializer': serializer, 'style': self.style})

    def post(self, request):
        serializer = RegisterSerializer(data=request.POST)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'style': self.style})
        serializer.save()
        return redirect('papapay.user:login')


class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/login.html'
    style = {'template_pack': 'user/serializers/horizontal'}

    def get(self, request):
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
