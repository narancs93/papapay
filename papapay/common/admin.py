from django.contrib import admin

from .models import PhoneNumber


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'phone_number', 'owner')
    search_fields = ('name', 'phone_number')
