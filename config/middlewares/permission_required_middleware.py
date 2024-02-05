from django.http import HttpResponseForbidden
from django.template import loader
from django.urls import resolve

from papapay.common.models import PageAccess


class PermissionRequiredMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        requested_view = resolve(request.path)
        required_permissions = self.get_required_permissions_for_view(requested_view)

        if not self.user_has_any_permission(request.user, required_permissions):
            return HttpResponseForbidden(loader.render_to_string("403.html"))

        return self.get_response(request)

    def get_required_permissions_for_view(self, requested_view):
        app_name = requested_view.app_names[-1] if requested_view.app_names else ''
        url_name = requested_view.url_name

        try:
            permissions = PageAccess.objects.get(
                app_name=app_name,
                url_name=url_name
            ).permissions.values('content_type__app_label', 'codename')
            return [f'{permission["content_type__app_label"]}.{permission["codename"]}' for permission in permissions]
        except PageAccess.DoesNotExist:
            return []

    def user_has_any_permission(self, user, permissions):
        if not permissions or user.is_superuser:
            return True

        user_permissions = user.get_user_permissions() | user.get_group_permissions()
        return bool(set(user_permissions).intersection(set(permissions)))
