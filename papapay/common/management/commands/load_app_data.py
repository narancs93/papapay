import pycountry
from django.core.management.base import BaseCommand

from papapay.postal_address.models import Country


class Command(BaseCommand):
    help = "Loads application data, e.g. countries"

    def handle(self, *args, **options):
        self.load_countries()

        self.stdout.write(
            self.style.SUCCESS('Application data loaded successfully')
        )

    def load_countries(self):
        for country in pycountry.countries:
            Country.objects.update_or_create(
                alpha3_code=country.alpha_3,
                defaults={
                    'name': country.name
                }
            )
