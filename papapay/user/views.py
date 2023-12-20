from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer

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
        return redirect('papapay.home:home-url')
