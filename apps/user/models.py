from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import EmailValidator
from simple_history.models import HistoricalRecords


class UserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def create_user(
        self,
        cnpj,
        email,
        password=None,
        **extra_fields,
    ):
        if not cnpj:
            raise ValueError("CNPJ is required.")
        if not email:
            raise ValueError("Company Fantasy is required.")

        email_validator = EmailValidator("Invalid email address.")
        email_validator(email)

        user = self.model(
            cnpj=cnpj,
            email=email,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        cnpj,
        email,
        password=None,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            cnpj,
            email,
            password,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True, editable=False, unique=True)
    cnpj = models.CharField(max_length=18, unique=True)
    email = models.EmailField(max_length=255, validators=[EmailValidator("Invalid email address.")], unique=True)

    email_secret = models.CharField(max_length=128, blank=True, null=True, unique=True)
    password_secret = models.CharField(max_length=128, blank=True, null=True, unique=True)

    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    history = HistoricalRecords()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_email_active = models.BooleanField(default=False)

    objects = UserManager()
    all_objects = models.Manager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "cnpj",
    ]

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def hard_delete(self, *args, **kwargs):
        super(User, self).delete(*args, **kwargs)
