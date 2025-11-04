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
    path('admin/category/create/', views.create_category, name='create_category'),
    path('admin/categories/', views.category_list, name='category_list'),
    path('admin/category/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path('admin/requests/', views.AllRequests.as_view(), name='all_requests'),
    path('admin/requests/<int:pk>/change_status/', views.ChangeRequestStatus.as_view(), name='change_status'),
]