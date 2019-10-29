from django.conf.urls import url, include
from django.urls import path, re_path
from . import  views
from django.urls import path

urlpatterns = [
	
	path(r'query/', views.query),
	path(r'query/bd', views.bd),
	path(r'', views.table_frombd),
	path(r'create_tables/', views.crt_html),
	re_path(r'change_data/test/$', views.new_data),
	re_path(r'del/$', views.del_data),
	re_path(r'change_data/$', views.change_data),
	re_path(r'add_data/new/$', views.add_data),
	re_path(r'add_data/$', views.add_data_name),
	re_path(r'truncate/$',views.truncate_table), 
	re_path(r'delete_table/$',views.delete_table),
	re_path(r'change_table/$',views.add_column),
	re_path(r'change_table/new/$',views.add_column_query),
	re_path(r'del_atrib/$',views.del_atrib),
	re_path(r'change_atrib/new/$',views.change_attrib),
	re_path(r'change_atrib/$',views.to_change_attrib),

]

