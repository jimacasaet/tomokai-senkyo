from django.conf.urls import patterns, include, url
from elect import views

from django.conf import settings


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^listing/', views.listing, name='listing'),
    url(r'^vote1/', views.vote_step1, name='vote1'),
    url(r'^vote2/', views.vote_step2, name='vote2'),
    url(r'^login/', views.site_login, name='login'),
    url(r'^logout/', views.site_logout, name='logout'),
    url(r'^change/', views.change, name='change'),
)