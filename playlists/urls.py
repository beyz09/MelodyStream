from django.urls import path
from . import views

urlpatterns = [
    path('playlists/', views.PlaylistListView.as_view(), name='playlist-list'),
    path('playlists/create/', views.PlaylistCreateView.as_view(), name='playlist-create'),
    path('playlists/<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist-detail'),
    path('playlists/<int:playlist_id>/add_song/<int:song_id>/', views.add_song_to_playlist, name='playlist-add-song'),
    path('songs/<int:song_id>/favorite/', views.add_to_favorites, name='add-to-favorites'),
] 