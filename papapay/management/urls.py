from django.urls import path

from . import views

app_name = 'papapay.management'

urlpatterns = [
    path('', views.Index.as_view(), name='management-page'),
    path('restaurants', views.ManageRestaurants.as_view(), name='manage-restaurants'),
    path('create-restaurant/', views.CreateRestaurant.as_view(), name='create-restaurant'),
    path('update-restaurant/<int:id>', views.UpdateRestaurant.as_view(), name='update-restaurant'),
]
