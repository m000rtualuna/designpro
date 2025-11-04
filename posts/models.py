from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from designpro import settings


class AdvUser(AbstractUser):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    patronymic = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    agreement = models.BooleanField(default=False, blank=False)

    class Meta:
        pass

STATUS = (
    ('n', 'Новая заявка'),
    ('a', 'Принято в работу'),
    ('d', 'Выполнено'),
)

class UserRequest(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/', blank=False, null=True)
    status = models.CharField(max_length=1, choices=STATUS, default='n')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)

class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title