from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.fields import ListField
from django.contrib.postgres.fields import ArrayField


class CustomPageNumberPagination(PageNumberPagination):
    page_size: int = 20
    page_size_query_param: str = "page_size"
    page_query_param: str = "page"
    max_page_size: int = 100

    def get_ordering(self, request):
        order = request.query_params.get("order", "desc")
        return "id" if order == "asc" else "-id"

    def paginate_queryset(self, queryset, request, view=None):
        ordering = self.get_ordering(request)
        queryset = queryset.order_by(ordering)
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "totalPages": self.page.paginator.num_pages,
                "currentPage": self.page.number,
                "perPage": self.get_page_size(self.request),
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )


def get_field_schema(field):
    type_mapping = {
        serializers.IntegerField: openapi.TYPE_INTEGER,
        serializers.CharField: openapi.TYPE_STRING,
        serializers.BooleanField: openapi.TYPE_BOOLEAN,
        serializers.FloatField: openapi.TYPE_NUMBER,
        serializers.DateField: openapi.TYPE_STRING,
        serializers.DateTimeField: openapi.TYPE_STRING,
        serializers.EmailField: openapi.TYPE_STRING,
        serializers.URLField: openapi.TYPE_STRING,
        serializers.UUIDField: openapi.TYPE_STRING,
        serializers.DecimalField: openapi.TYPE_NUMBER,
        serializers.ImageField: openapi.TYPE_STRING,
        serializers.FileField: openapi.TYPE_STRING,
        serializers.JSONField: openapi.TYPE_OBJECT,
        serializers.ListField: openapi.TYPE_ARRAY,
    }

    if isinstance(field, serializers.ListSerializer) or isinstance(field, ArrayField) or isinstance(field, ListField):
        child_schema = (
            get_field_schema(field.child) if hasattr(field, "child") else openapi.Schema(type=openapi.TYPE_STRING)
        )
        return openapi.Schema(type=openapi.TYPE_ARRAY, items=child_schema)
    elif isinstance(field, serializers.ModelSerializer):
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={field_name: get_field_schema(sub_field) for field_name, sub_field in field.fields.items()},
        )
    else:
        field_type = type_mapping.get(type(field), openapi.TYPE_STRING)
        return openapi.Schema(type=field_type)


def get_paginated_response_schema(serializer_class):
    serializer = serializer_class()
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "count": openapi.Schema(type=openapi.TYPE_INTEGER, description="Total number of items"),
            "totalPages": openapi.Schema(type=openapi.TYPE_INTEGER, description="Total number of pages"),
            "currentPage": openapi.Schema(type=openapi.TYPE_INTEGER, description="Current page number"),
            "perPage": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of items per page"),
            "next": openapi.Schema(
                type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description="Link to the next page"
            ),
            "previous": openapi.Schema(
                type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description="Link to the previous page"
            ),
            "results": openapi.Schema(
                type=openapi.TYPE_ARRAY, items=get_field_schema(serializer), description="List of results"
            ),
        },
    )


def get_pagination_manual_params():
    return [
        openapi.Parameter(
            name="order",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            enum=["asc", "desc"],
            description="Order results by ascending or descending ID",
        ),
        openapi.Parameter(
            "fields",
            openapi.IN_QUERY,
            description="Comma-separated list of fields to include in the response",
            type=openapi.TYPE_STRING,
        ),
    ]
