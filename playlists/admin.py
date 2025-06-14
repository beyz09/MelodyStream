from django.contrib import admin
from .models import Playlist, PlaylistSong, Favorite, ListeningHistory

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('playlist_name', 'user', 'is_public', 'created_at')
    list_filter = ('is_public', 'user')
    search_fields = ('playlist_name', 'user__username')
    raw_id_fields = ('user',)

@admin.register(PlaylistSong)
class PlaylistSongAdmin(admin.ModelAdmin):
    list_display = ('playlist', 'song', 'added_at', 'order_index')
    list_filter = ('playlist', 'song')
    raw_id_fields = ('playlist', 'song')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'song', 'created_at')
    search_fields = ('user__username', 'song__song_name')
    raw_id_fields = ('user', 'song')

@admin.register(ListeningHistory)
class ListeningHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'song', 'listened_at', 'duration_listened')
    search_fields = ('user__username', 'song__song_name')
    raw_id_fields = ('user', 'song') 