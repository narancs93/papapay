from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit
from django import forms

from papapay.postal_address.models import Country
from papapay.postal_address.utils import create_postal_address
from papapay.restaurant.models import Restaurant


class RestaurantForm(forms.ModelForm):
    country = forms.ChoiceField(choices=[])
    state = forms.CharField(max_length=255)
    zip_code = forms.CharField(max_length=16)
    city = forms.CharField(max_length=255)
    district = forms.CharField(max_length=255, required=False)
    street = forms.CharField(max_length=255)
    house_number = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].choices = [
            (country.name, country.name) for country in Country.objects.all().order_by('name')]
        self.helper = FormHelper()
        self.helper.form_id = 'update-restaurant-form'
        self.helper.form_method = 'post'
        self.helper.label_class = 'text-lg font-semibold text-white pb-2'

        self.helper.layout = Layout(
            Field('name', css_class='mt-2 mb-4'),
            Field('email_address', css_class='mt-2 mb-4'),
            Field('description', css_class='mt-2 mb-4'),
            Field('introduction', css_class='mt-2 mb-4'),
            Field('country', css_class='mt-2 mb-4'),
            Field('state', css_class='mt-2 mb-4'),
            Field('zip_code', css_class='mt-2 mb-4'),
            Field('city', css_class='mt-2 mb-4'),
            Field('district', css_class='mt-2 mb-4'),
            Field('street', css_class='mt-2 mb-4'),
            Field('house_number', css_class='mt-2 mb-4'),
        )

        self.fields['description'].required = False
        self.fields['introduction'].required = False

        self.helper.add_input(Submit(
            name='submit',
            value='Save',
            css_class='bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded'))

    def set_postal_address(self, post_data):
        address = create_postal_address(
            country_name=post_data.get('country'),
            state_name=post_data.get('state'),
            city_name=post_data.get('city'),
            district_name=post_data.get('district') or '-',
            street_zip_code=post_data.get('zip_code'),
            street_name=post_data.get('street'),
            house_number=post_data.get('house_number'),
            )
        self.instance.postal_address = address


    class Meta:
        model = Restaurant
        fields = ['name', 'email_address', 'description', 'introduction']
