from ..postal_address.models import (City, Country, District, PostalAddress,
                                     State, Street)


def create_postal_address(*,
                          country_name, state_name, city_name, district_name,
                          street_zip_code, street_name, house_number, **fields):
    """
        Creates a PostalAddress object and other ForeignKey dependencies.

        Args (mandatory):
        - country_name (str): name of the country
        - state_name (str): name of the state
        - city_name (str): name of the city
        - district_name (str): name of the district
        - street_zip_code (str): ZIP code of the street
        - street_name (str): name of the street
        - house_number (str)

        Args (optional):
        - country_alpha3_code (str, optional): alpha 3 code of the country
        - country_call_prefix (str, optional): international call prefix of the country
        - state_abbreviation (str, optional): abbreviation of the state name
        - state_area_code (str, optional): area code of the state
        - floor_number (str, optional)
        - door_number (str, optional)
        - note (str, optional)
    """

    country, _ = Country.objects.get_or_create(
        name=country_name,
        defaults={
            'alpha3_code': fields.get('country_alpha3_code', ''),
            'international_call_prefix': fields.get('country_call_prefix', '')
        }
    )

    state, _ = State.objects.get_or_create(
        country=country,
        name=state_name,
        defaults={
            'abbreviation': fields.get('state_abbreviation', ''),
            'area_code': fields.get('state_area_code', '')
        }
    )

    city, _ = City.objects.get_or_create(
        state=state,
        name=city_name
    )

    district, _ = District.objects.get_or_create(
        city=city,
        name=district_name
    )

    street, _ = Street.objects.get_or_create(
        district=district,
        name=street_name,
        defaults={
            'zip_code': street_zip_code
        }
    )

    postal_address, _ = PostalAddress.objects.get_or_create(
        street=street,
        house_number=house_number,
        floor_number=fields.get('floor_number', ''),
        door_number=fields.get('door_number', ''),
        note=fields.get('note', '')
    )

    return postal_address
