from rest_framework import serializers
from .models import AbstractBaseModel
from django.contrib.auth import get_user_model

User = get_user_model()


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set()
            nested_fields = {}

            for field in fields:
                parts = field.split(".")
                parent = parts[0]

                if len(parts) > 1:
                    child = ".".join(parts[1:])
                    if parent not in nested_fields:
                        nested_fields[parent] = []
                    nested_fields[parent].append(child)
                else:
                    allowed.add(field)

            existing = set(self.fields)

            for parent, children in nested_fields.items():
                allowed.add(parent)
                if parent in self.fields:
                    if isinstance(self.fields[parent], serializers.ListSerializer):
                        child_serializer = self.fields[parent].child.__class__(*args, **{"fields": children})
                        self.fields[parent].child = child_serializer
                    else:
                        nested_serializer = self.fields[parent].__class__(*args, **{"fields": children})
                        self.fields[parent] = nested_serializer

            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "cnpj",
            "company_fantasy",
            "company_name",
            "company_email",
            "company_phone",
            "company_address",
            "agent_name",
            "agent_cpf",
            "agent_office",
            "agent_phone",
            "is_active",
        ]
        read_only_fields = ["id"]


class BaseSerializer(DynamicFieldsModelSerializer):
    is_active = serializers.BooleanField(required=False, default=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = AbstractBaseModel
        fields = "__all__"

    def get_user(self, obj):
        if obj.user:
            return UserSerializer(obj.user).data
        return None

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return internal_value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

    def save(self, **kwargs):
        request = self.context.get("request")
        if request and hasattr(request, "user_id"):
            user = User.all_objects.get(id=request.user_id)
            self.validated_data["user"] = user
        return super().save(**kwargs)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
