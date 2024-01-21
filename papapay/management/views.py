from django.views.generic import TemplateView

from papapay.restaurant.models import Restaurant


class Index(TemplateView):
    template_name = 'management/index.html'


class ManageRestaurants(TemplateView):
    template_name = 'management/restaurants.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant_count'] = Restaurant.objects.count()
        return context
