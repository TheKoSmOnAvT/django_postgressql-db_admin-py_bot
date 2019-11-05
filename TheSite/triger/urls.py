from django.conf.urls import url, include
from django.urls import path, re_path
from . import  views
from django.urls import path

urlpatterns = [
	
	path(r'', views.print_trigers),
	path(r'to_trig/', views.print_trigers),
	re_path(r'create_triger/new/', views.create_trig_in_bd),
	re_path(r'create_triger/', views.create_trig_html),
	re_path(r'to_trig/on_triger/$',  views.on_trig),
	re_path(r'to_trig/off_triger/$',  views.off_trig),
	re_path(r'to_trig/del_triger/$',  views.del_trig)
]

