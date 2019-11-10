from django.conf.urls import url, include
from django.urls import path, re_path
from . import  views
from django.urls import path

urlpatterns = [
	
	path(r'', views.print_views),
	path(r'to_view/', views.print_views),
	re_path(r'to_view/del_view/$', views.del_views),
	re_path(r'create_view$', views.to_create_view),
	re_path(r'new/$', views.create_view),
	# path(r'to_trig/', views.print_trigers),  create_view
	# re_path(r'create_triger/new/', views.create_trig_in_bd),
	# re_path(r'create_triger/', views.create_trig_html),
	# re_path(r'to_trig/on_triger/$',  views.on_trig),
	# re_path(r'to_trig/off_triger/$',  views.off_trig),
	# re_path(r'to_trig/del_triger/$',  views.del_trig)
]

