from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns=[
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login_user/$', views.login_user, name='login_user'),
	url(r'^logout_user/$', views.logout_user, name="logout_user"),
	url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
	url(r'album/add/$', views.AlbumCreate.as_view(), name="album-add"),
	url(r'album/(?P<pk>\d+)/$', views.AlbumUpdate.as_view(), name="album-update"),
	url(r'album/(?P<pk>\d+)/delete/$', views.AlbumDelete.as_view(), name="album-delete"),
	url(r'album/(?P<album_id>\d+)/song/add/$', views.create_song, name="song-add"),
]