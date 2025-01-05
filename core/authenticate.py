from rest_framework_simplejwt import authentication as jwt_authentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
from .permissions import CustomAuthenticationFailed


def enforce_csrf(request):
    csrf_token = request.COOKIES.get("csrftoken")

    if csrf_token:
        request.META["HTTP_X_CSRFTOKEN"] = csrf_token
    else:
        raise CustomAuthenticationFailed(detail="CSRF Failed")

    csrf_middleware = CsrfViewMiddleware(lambda req: None)
    response = csrf_middleware.process_view(request, None, (), {})
    if response:
        raise CustomAuthenticationFailed(detail="CSRF Failed")


class CustomAuthentication(jwt_authentication.JWTAuthentication):
    def authenticate(self, request):
        if (
            request.path.startswith("/admin/")
            or request.path.startswith("/swagger/")
            or request.path.startswith("/redoc/")
        ):
            return None

        access = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"]) or None

        if not access:
            raise InvalidToken("No valid access token found.")

        validated_token = self.get_validated_token(access)
        enforce_csrf(request)
        request.user_id = validated_token["user_id"]
        return self.get_user(validated_token), validated_token
