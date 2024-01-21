from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from .forms import RestaurantForm
from ..restaurant.models import Restaurant


class Index(TemplateView):
    template_name = 'management/index.html'


class ManageRestaurants(TemplateView):
    template_name = 'management/restaurants.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurants'] = Restaurant.objects.all()
        return context


class UpdateRestaurant(TemplateView):
    template_name = 'management/update_restaurant.html'

    def get_context_data(self, id, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = get_object_or_404(Restaurant, id=id)
        context['restaurant_form'] = RestaurantForm(instance=restaurant)
        return context

    def post(self, request, id, **kwargs):
        restaurant = get_object_or_404(Restaurant, id=id)
        restaurant_form = RestaurantForm(data=request.POST, instance=restaurant)
        if restaurant_form.is_valid():
            restaurant_form.save()
        return render(self.request, 'management/update_restaurant.html', context={
            'restaurant_form': restaurant_form,
            'updated_result': 'success' if restaurant_form.is_valid() else 'error',
        })
