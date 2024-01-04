from django.contrib import admin

from .models import City, Country, District, PostalAddress, State, Street


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'alpha2_code', 'alpha3_code')
    search_fields = ('name', 'alpha2_code', 'alpha3_code')


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'abbreviation', 'area_code', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'abbreviation', 'area_code', 'country')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'state')
    list_filter = ('state__country', 'state')
    search_fields = ('name', 'state')


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city')
    list_filter = ('city',)
    search_fields = ('name', 'city')


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ('id', 'zip_code', 'name', 'district')
    list_filter = ('district__city', 'district')
    search_fields = ('zip_code', 'name', 'district')


@admin.register(PostalAddress)
class PostalAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'street', 'house_number', 'floor_number', 'door_number', 'note')
    search_fields = ('street', 'house_number', 'floor_number', 'door_number', 'note')
