from django.contrib import admin
from .models import AdvUser, UserRequest, Category, Comment

admin.site.register(AdvUser)
admin.site.register(UserRequest)
admin.site.register(Category)
admin.site.register(Comment)