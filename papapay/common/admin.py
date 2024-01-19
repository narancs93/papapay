from django.contrib import admin

from .models import PageAccess, PhoneNumber


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'phone_number', 'owner')
    search_fields = ('name', 'phone_number')


@admin.register(PageAccess)
class PageAccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'app_name', 'url_name')
    search_fields = ('app_name', 'url_name')
