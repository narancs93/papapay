from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit
from django import forms

from papapay.restaurant.models import Restaurant


class RestaurantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'update-restaurant-form'
        self.helper.form_method = 'post'
        self.helper.label_class = 'text-lg font-semibold text-white pb-2'

        self.helper.layout = Layout(
            Field('name', css_class='mt-2 mb-4'),
            Field('email_address', css_class='mt-2 mb-4'),
            Field('description', css_class='mt-2 mb-4'),
            Field('introduction', css_class='mt-2 mb-4'),
        )

        self.fields['description'].required = False
        self.fields['introduction'].required = False

        self.helper.add_input(Submit(
            name='submit',
            value='Save',
            css_class='bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded'))

    class Meta:
        model = Restaurant
        fields = ['name', 'email_address', 'description', 'introduction']
