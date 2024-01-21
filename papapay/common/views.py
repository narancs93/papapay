from django.views.generic import TemplateView


class PermissionDeniedPage(TemplateView):
    template_name = '403.html'
