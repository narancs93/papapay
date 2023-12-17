from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=64, unique=True)
    initials = models.CharField(max_length=3, blank=True)

    def __str__(self):
        return f'{self.name} (id={self.id})'

    class Meta:
        verbose_name_plural = 'Countries'


class State(models.Model):
    name = models.CharField(max_length=100)
    initials = models.CharField(max_length=3, blank=True)
    area_code = models.CharField(max_length=10, blank=True)
    country = models.ForeignKey(Country, related_name='states', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} ({self.country.name}) (id={self.id})'

    class Meta:
        unique_together = ('name', 'country')


class City(models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, related_name='cities', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} ({self.state.name}) (id={self.id})'

    class Meta:
        verbose_name_plural = 'Cities'
        unique_together = ('name', 'state')


class District(models.Model):
    name = models.CharField(max_length=128)
    city = models.ForeignKey(City, related_name='districts', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} ({self.city.name}) (id={self.id})'

    class Meta:
        unique_together = ('name', 'city')


class Street(models.Model):
    zip_code = models.CharField(max_length=12)
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, related_name='streets', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} ({self.district.name}) (id={self.id})'

    class Meta:
        unique_together = ('name', 'district')


class PostalAddress(models.Model):
    street = models.ForeignKey(Street, related_name='postal_addresses', on_delete=models.PROTECT)
    house_number = models.CharField(max_length=16)
    floor_number = models.CharField(max_length=10, blank=True)
    door_number = models.CharField(max_length=20, blank=True)
    note = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.street.name}, {self.house_number}, {self.floor_number}/{self.door_number} (id={self.id})'

    class Meta:
        verbose_name_plural = 'Postal Addresses'
