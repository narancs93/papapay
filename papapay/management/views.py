from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, ListView, TemplateView

from papapay.postal_address.utils import create_postal_address

from ..restaurant.models import Restaurant
from .forms import RestaurantForm


class Index(TemplateView):
    template_name = 'management/index.html'


class ManageRestaurants(ListView):
    template_name = 'management/restaurants.html'
    model = Restaurant
    context_object_name = 'restaurants'


class CreateRestaurant(CreateView):
    template_name = 'management/create_restaurant.html'
    success_url = '/management/restaurants'
    model = Restaurant
    form_class = RestaurantForm

    def get_form(self):
        form = super().get_form()
        if self.request.method == 'POST':
            form.set_postal_address(self.request.POST)
        return form


class UpdateRestaurant(TemplateView):
    template_name = 'management/update_restaurant.html'

    def get_context_data(self, id, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = get_object_or_404(Restaurant, id=id)
        context['restaurant_form'] = RestaurantForm(instance=restaurant, initial={
            'country': restaurant.postal_address.street.district.city.state.country.name,
            'state': restaurant.postal_address.street.district.city.state.name,
            'city': restaurant.postal_address.street.district.city.name,
            'district': restaurant.postal_address.street.district.name,
            'zip_code': restaurant.postal_address.street.zip_code,
            'street': restaurant.postal_address.street.name,
            'house_number': restaurant.postal_address.house_number,
        })
        return context

    def post(self, request, id, **kwargs):
        address = create_postal_address(
            country_name=request.POST.get('country'),
            state_name=request.POST.get('state'),
            city_name=request.POST.get('city'),
            district_name=request.POST.get('district') or '-',
            street_zip_code=request.POST.get('zip_code'),
            street_name=request.POST.get('street'),
            house_number=request.POST.get('house_number'),
        )

        post_data = request.POST.copy()
        post_data['postal_address'] = address
        restaurant = get_object_or_404(Restaurant, id=id)
        restaurant_form = RestaurantForm(data=post_data, instance=restaurant)
        if restaurant_form.is_valid():
            restaurant_form.save()
        return render(self.request, 'management/update_restaurant.html', context={
            'restaurant_form': restaurant_form,
            'updated_result': 'success' if restaurant_form.is_valid() else 'error',
        })
