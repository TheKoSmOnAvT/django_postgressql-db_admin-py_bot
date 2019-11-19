from django.conf.urls import url, include
from django.urls import path, re_path
from . import  views
from django.urls import path

urlpatterns = [
    path(r'', views.to_func),
    path(r'to_func/', views.to_func),
    re_path(r'to_func/del_func/$', views.del_func),
    re_path(r'create_func$', views.to_create_html),
    re_path(r'new/$', views.create_func),
]
    