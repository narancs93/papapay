from django.urls import path

from . import views

app_name = 'papapay.management'

urlpatterns = [
    path('', views.Index.as_view(), name='management-page'),
]
