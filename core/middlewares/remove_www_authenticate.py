from django.utils.deprecation import MiddlewareMixin


class RemoveWWWAuthenticateHeaderMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 401:
            if "WWW-Authenticate" in response.headers:
                del response.headers["WWW-Authenticate"]
        return response
