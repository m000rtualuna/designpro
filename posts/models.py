from django.contrib.auth.models import AbstractUser
from django.db import models


class AdvUser(AbstractUser):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    patronymic = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    agreement = models.BooleanField(default=False, blank=False)

    class Meta:
        pass
