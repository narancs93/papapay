from django.core.management.base import BaseCommand

from phonenumbers import country_code_for_region

from pycountry import countries as py_countries

from papapay.postal_address.models import Country


class Command(BaseCommand):
    help = "Loads application data, e.g. countries"

    def handle(self, *args, **options):
        self.load_countries()
        self.load_international_call_prefixes()

        self.stdout.write(
            self.style.SUCCESS('Application data loaded successfully')
        )

    def load_countries(self):
        for country in py_countries:
            Country.objects.update_or_create(
                alpha3_code=country.alpha_3,
                defaults={
                    'alpha2_code': country.alpha_2,
                    'name': country.name
                }
            )

    def load_international_call_prefixes(self):
        for country in py_countries:
            country_code = country.alpha_2
            call_prefix = country_code_for_region(country_code)
            try:
                country_obj = Country.objects.get(alpha3_code=country.alpha_3)
                country_obj.international_call_prefix = f'+{call_prefix}'
                country_obj.save()
            except Country.DoesNotExist:
                pass
