from django.urls import path

from . import views

app_name = 'papapay.user'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('api/profile/remove-phone-number', views.RemovePhoneNumberFromUser.as_view(),
         name='remove-phone-number-from-profile-api'),
]
