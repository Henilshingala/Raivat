from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from jewelry import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jewelry.urls')),
]

handler404 = views.page_not_found


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
