from django.views.generic import CreateView, ListView, TemplateView, UpdateView

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


class UpdateRestaurant(UpdateView):
    template_name = 'management/update_restaurant.html'
    success_url = '/management/restaurants'
    model = Restaurant
    form_class = RestaurantForm

    def get_form(self, *args, **kwargs):
        form = super().get_form()
        if self.request.method == 'POST':
            form.set_postal_address(self.request.POST)
        return form
