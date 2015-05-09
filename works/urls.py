from django.conf.urls import patterns, url
from works import views
from django.conf import settings

urlpatterns = patterns('',
    url(r'^about/$', views.about, name='about'),
    url(r'^$', views.index, name='index'),
    url(r'^board/(?P<board_name_slug>[\w\-]+)/$', views.board, name='board'),)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}),)