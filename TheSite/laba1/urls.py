from django.conf.urls import url, include
from . import  views
from django.urls import path

urlpatterns = [
	path('', views.index),
	path(r'query/', views.query),
	path(r'query/bd', views.bd),

]
