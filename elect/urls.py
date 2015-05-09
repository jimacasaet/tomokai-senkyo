from django.conf.urls import patterns, include, url
from elect import views

from django.conf import settings


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^listing/', views.registered, name='registered'),
    url(r'^vote/', views.vote, name='vote'),
    url(r'^receive/', views.receive, name='receive'),
)