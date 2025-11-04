from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.UsersRequestListView.as_view(), name='index'),
    path('accounts/login', views.PostsLoginView.as_view(), name='login'),
    path('accounts/registration', views.register, name='registration'),
    path('accounts/profile', views.profile, name='profile'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('create_request/', views.create_request, name='create_request'),
    path('request/<int:pk>', views.RequestDetail.as_view(), name='request_detail'),
    path('request/<int:pk>/delete/', views.DeleteRequest.as_view(), name='request_delete'),
]