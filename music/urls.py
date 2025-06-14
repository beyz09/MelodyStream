from django.urls import path
from . import views

urlpatterns = [
    path('songs/', views.SongListAPIView.as_view(), name='song-list'),
    path('songs/<int:pk>/', views.SongDetailAPIView.as_view(), name='song-detail'),
    path('songs/search/', views.search_songs, name='search-songs'),
    path('songs/<int:song_id>/play/', views.play_song, name='play-song'),
] 