from django.contrib import admin
from .models import AdvUser, UserRequest, Category

admin.site.register(AdvUser)
admin.site.register(UserRequest)
admin.site.register(Category)