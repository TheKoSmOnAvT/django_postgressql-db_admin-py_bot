from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', include('TheFirst.urls')),
    path(r'laba1/', include('laba1.urls')),
    path(r'triger/', include('triger.urls')),
    path(r'views/', include('views.urls')),
    path(r'func/', include('functions.urls')),
]
    