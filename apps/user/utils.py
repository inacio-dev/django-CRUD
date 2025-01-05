from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt import tokens


def get_user_tokens(user):
    if not user.is_active:
        raise AuthenticationFailed("User is not active.")

    refresh = tokens.RefreshToken.for_user(user)

    access = refresh.access_token
    access["id"] = user.id

    return {"refresh_token": str(refresh), "access_token": str(access)}
