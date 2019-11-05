from django.conf.urls import url, include
from . import  views
from django.urls import path


urlpatterns = [
	url(r'^$', views.lend, name='lend')
	#url(r'/trigers', views.lend, name='lend')
]
