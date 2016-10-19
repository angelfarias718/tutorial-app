from django.conf.urls import patterns, include, url 
from tutorial_app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'))