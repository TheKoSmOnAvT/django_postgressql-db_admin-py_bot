from django.conf.urls import url, include
from django.urls import path, re_path
from . import  views
from django.urls import path

urlpatterns = [
	
	path(r'query/', views.query),
	path(r'query/bd', views.bd),
	path(r'', views.table_frombd),
	re_path(r'change_data/test/$', views.new_data),
	re_path(r'del/$', views.del_data),
	re_path(r'change_data/$', views.change_data),
	re_path(r'add_data/new/$', views.add_data),
	re_path(r'add_data/$', views.add_data_name),
]
