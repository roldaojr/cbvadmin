from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cbvadmin.sites import site as admin

urlpatterns = [
    path('', admin.urls),
]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
