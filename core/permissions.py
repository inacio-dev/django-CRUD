from rest_framework import permissions
from django.conf import settings
from rest_framework.exceptions import APIException


class AccessPermission(permissions.BasePermission):
    def __init__(self):
        self.message = "Acesso negado."

    def has_permission(self, request, view):
        access_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"]) or None

        if not access_token:
            self._deny_permission("Nenhum token de autenticação fornecido.")
            return False

        view.access_token = access_token
        return True

    def _deny_permission(self, message):
        raise CustomAuthenticationFailed(detail=message)


class RefreshPermission(permissions.BasePermission):
    def __init__(self):
        self.message = "Acesso negado."

    def has_permission(self, request, view):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"]) or None

        if not refresh_token:
            self._deny_permission("Nenhum token de autenticação fornecido.")
            return False

        view.refresh_token = refresh_token
        return True

    def _deny_permission(self, message):
        raise CustomAuthenticationFailed(detail=message)


class CustomAuthenticationFailed(APIException):
    status_code = 401
    default_detail = "Não autorizado."
    default_code = "not_authenticated"
