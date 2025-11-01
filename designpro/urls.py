from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('posts.urls')),
    path('', RedirectView.as_view(url='posts/', permanent=True)),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)