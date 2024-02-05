from django.urls import reverse
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import RestaurantForm
from ..restaurant.models import Restaurant


class Index(TemplateView):
    template_name = 'management/index.html'


class ManageRestaurants(ListView):
    template_name = 'management/restaurants.html'
    model = Restaurant
    context_object_name = 'restaurants'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["delete_restaurant_api"] = reverse('papapay.management:delete-restaurant-api')
        return context


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


class DeleteRestaurant(APIView):

    def post(self, request, *args, **kwargs):
        try:
            Restaurant.objects.get(id=request.data.get('id')).delete()
            return Response(status=status.HTTP_200_OK)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
