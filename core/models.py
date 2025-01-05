from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth import get_user_model

User = get_user_model()


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class AbstractBaseModel(models.Model):
    is_active: bool = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    history = HistoricalRecords(inherit=True)

    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    objects = models.Manager()
    active_objects = ActiveManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def hard_delete(self, *args, **kwargs):
        super(AbstractBaseModel, self).delete(*args, **kwargs)
