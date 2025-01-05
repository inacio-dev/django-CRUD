import secrets

from rest_framework import serializers
from core.serializers import DynamicFieldsModelSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import User
from .utils import get_user_tokens


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)


class RegisterSerializer(serializers.Serializer):
    cnpj = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserSerializer(DynamicFieldsModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    email_secret = serializers.CharField(read_only=True)

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
            "email_secret",
            "password",
        ]

    def create(self, validated_data):
        while True:
            email_secret = secrets.token_hex(64)
            if not User.all_objects.filter(email_secret=email_secret).exists():
                break
        validated_data["email_secret"] = email_secret

        user = User.objects.create_user(**validated_data)

        return user


class EmailSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)


class ConfirmEmailSerializer(serializers.Serializer):
    emailSecret = serializers.CharField(required=True)


class ConfirmPasswordSerializer(serializers.Serializer):
    passwordSecret = serializers.CharField(required=True)
    newPassword = serializers.CharField(style={"input_type": "password"}, write_only=True, required=True)


class PasswordResetSerializer(serializers.Serializer):
    password_secret = serializers.CharField(max_length=128)
    new_password = serializers.CharField(style={"input_type": "password"}, write_only=True)


class UserResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    cnpj = serializers.CharField(read_only=True)
    companyFantasy = serializers.CharField(read_only=True)
    companyName = serializers.CharField(read_only=True)
    companyEmail = serializers.CharField(read_only=True)
    companyPhone = serializers.CharField(read_only=True)
    companyAddress = serializers.CharField(read_only=True)
    agentName = serializers.CharField(read_only=True)
    agentCpf = serializers.CharField(read_only=True)
    agentOffice = serializers.CharField(read_only=True)
    agentPhone = serializers.CharField(read_only=True)


class EditUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    cnpj = serializers.CharField(required=False)
    companyFantasy = serializers.CharField(required=False)
    companyName = serializers.CharField(required=False)
    companyEmail = serializers.CharField(required=False)
    companyPhone = serializers.CharField(required=False)
    companyAddress = serializers.CharField(required=False)
    agentName = serializers.CharField(required=False)
    agentCpf = serializers.CharField(required=False)
    agentOffice = serializers.CharField(required=False)
    agentPhone = serializers.CharField(required=False)


class EditUserRequestSerializer(DynamicFieldsModelSerializer):

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
        extra_kwargs = {
            "cnpj": {"required": False},
            "company_fantasy": {"required": False},
            "company_name": {"required": False},
            "company_email": {"required": False},
            "company_phone": {"required": False},
            "company_address": {"required": False},
            "agent_name": {"required": False},
            "agent_cpf": {"required": False},
            "agent_office": {"required": False},
            "agent_phone": {"required": False},
            "is_active": {"required": False},
        }
        read_only_fields = ["id"]


class PasswordSetSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(style={"input_type": "password"}, write_only=True)
    newPassword = serializers.CharField(style={"input_type": "password"}, write_only=True)
    confirmPassword = serializers.CharField(style={"input_type": "password"}, write_only=True)


class PasswordSetRequestSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    new_password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    confirm_password = serializers.CharField(style={"input_type": "password"}, write_only=True)


class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        refresh_token = self.context.get("refresh_token")

        if not refresh_token:
            raise InvalidToken("No valid refresh token found.")

        try:
            token = RefreshToken(refresh_token)
            user = User.all_objects.get(id=token["user_id"])

            if not user.is_active:
                raise AuthenticationFailed("Usuário não está ativo.")

            new_tokens = get_user_tokens(user)

            return {"access_token": new_tokens["access_token"], "refresh_token": new_tokens["refresh_token"]}
        except TokenError as e:
            raise InvalidToken("Invalid refresh token.") from e
        except User.DoesNotExist:
            raise InvalidToken("User not found.")

    @property
    def fields(self):
        return {}
