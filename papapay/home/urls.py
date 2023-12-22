from django.urls import path

from .views import Home

app_name = 'papapay.home'

urlpatterns = [
    path('', Home.as_view(), name='home-url'),
]
