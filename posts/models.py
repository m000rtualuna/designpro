import os
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
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

ALLOWED_USERREQUEST_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp']

def validate_userrequest_image_extension(value):
    ext=os.path.splitext(value.name)[1].lower()
    if ext not in ALLOWED_USERREQUEST_IMAGE_EXTENSIONS:
        raise ValidationError('Неккоректный формат изображения')

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
    image = models.ImageField(upload_to='media/', blank=False, null=True, validators=[validate_userrequest_image_extension])
    status = models.CharField(max_length=1, choices=STATUS, default='n')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)

    #def set_status(self, new_status):
     #   if new_status in ['a', 'd'] and self.status != 'n':
      #      return False
       # return True


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title