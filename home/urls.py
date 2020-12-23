from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signup/$', views.UserFormView.as_view(), name='signup'),
    url(r'^select/$', views.SelectView.as_view(), name='select'),
    url(r'^songs/$', views.songs, name='songs'),
    url(r'^player/$', views.player, name='player'),
    url(r'^loginselect/$', views.LoginSelectView.as_view(), name='loginselect'),
    url(r'^addplaylist/$', views.IndexView.as_view(), name='addplaylist'),
    url(r'^playlist/add/$', views.PlaylistCreate.as_view(), name='playlist-add'),
    url(r'^playlist/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^playlist/(?P<pk>[0-9]+)/delete/$', views.PlaylistDelete.as_view(), name='playlist-delete'),
    url(r'^playlistsong/add/$', views.PlaylistsongCreate.as_view(), name='playlistsong-add'),
    url(r'^playlistsong/(?P<pk>[0-9]+)/delete/$', views.PlaylistsongDelete.as_view(), name='playlistsong-delete'),
]
