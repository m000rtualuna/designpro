from django.urls import path
from . import views
from .views import PostsLoginView

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login', PostsLoginView.as_view(), name='login'),
    path('accounts/registration', views.register, name='registration'),
]