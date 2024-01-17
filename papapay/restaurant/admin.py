from django.contrib import admin

from .models import Restaurant, SocialMediaAccount


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email_address', 'postal_address']


@admin.register(SocialMediaAccount)
class SocialMediaAccountAdmin(admin.ModelAdmin):
    list_display = ['platform', 'username', 'restaurant']
