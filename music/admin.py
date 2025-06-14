from django.contrib import admin
from .models import Artist, Album, Song

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('artist_name', 'country', 'genre', 'is_active')
    search_fields = ('artist_name', 'country', 'genre')

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('album_name', 'artist', 'release_date', 'genre', 'total_tracks')
    list_filter = ('genre', 'release_date')
    search_fields = ('album_name', 'artist__artist_name')
    raw_id_fields = ('artist',)

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('song_name', 'artist', 'album', 'duration_seconds', 'play_count')
    list_filter = ('artist', 'album')
    search_fields = ('song_name', 'artist__artist_name', 'album__album_name')
    raw_id_fields = ('artist', 'album') 