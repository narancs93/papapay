from django.db import models

from papapay.postal_address.models import PostalAddress


class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    introduction = models.TextField(blank=True)
    email_address = models.EmailField()
    postal_address = models.ForeignKey(PostalAddress, related_name='restaurants', on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} (id={self.id})'


class SocialMediaAccount(models.Model):
    SOCIAL_MEDIA_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('tripadvisor', 'Tripadvisor')
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=SOCIAL_MEDIA_CHOICES)
    username = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.restaurant.name}'s {self.get_platform_display()} Account: {self.username}"

    class Meta:
        unique_together = ('platform', 'username')
