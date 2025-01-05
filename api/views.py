from rest_framework.decorators import permission_classes, authentication_classes
from django.http import JsonResponse


@authentication_classes([])
@permission_classes([])
def health_check(request):
    return JsonResponse({"status": "healthy"}, status=200)


@authentication_classes([])
@permission_classes([])
def home(request):
    return JsonResponse({"message": "Welcome to api API"})
