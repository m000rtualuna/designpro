from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include
from django.views.generic import RedirectView
from django.views.decorators.cache import never_cache
from django.views.static import serve

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('catalog/', include('posts.urls')),
    path('', RedirectView.as_view(url='posts/', permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
