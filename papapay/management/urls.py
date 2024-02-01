from django.urls import path

from . import views

app_name = 'papapay.management'

html_urls = [
    path('', views.Index.as_view(), name='management-page'),
    path('restaurants', views.ManageRestaurants.as_view(), name='manage-restaurants'),
    path('create-restaurant/', views.CreateRestaurant.as_view(), name='create-restaurant'),
    path('update-restaurant/<int:pk>', views.UpdateRestaurant.as_view(), name='update-restaurant'),
]

api_urls = [
    path('api/delete-restaurant', views.DeleteRestaurant.as_view(), name='delete-restaurant-api'),
]

urlpatterns = html_urls + api_urls
