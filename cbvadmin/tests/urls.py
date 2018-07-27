from django.conf.urls import url
from django.contrib import admin
import cbvadmin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', cbvadmin.site.urls),
]
