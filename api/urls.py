from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from .views import health_check, home
from decouple import config

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version=config("VERSION", default="v1", cast=str),
        description="Models",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=config("BASE_URL", cast=str),
)

urlpatterns = [
    path("", home, name="home"),
    path("health/", health_check, name="health-check"),
    path("api/user/", include("apps.user.urls")),
    path("api/product/", include("apps.product.urls")),
    path("api/cart", include("apps.cart.urls")),
    path("api/address", include("apps.address.urls")),
    path("api/purchase/", include("apps.purchase.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("admin/", admin.site.urls),
        re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
        re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
        re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    ]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
