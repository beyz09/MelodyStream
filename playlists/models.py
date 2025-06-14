from django.db import models
from authentication.models import User
from music.models import Song

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    playlist_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_public = models.BooleanField(default=False)
    songs = models.ManyToManyField(Song, through='PlaylistSong', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.playlist_name} - {self.user.username}"

class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    order_index = models.IntegerField(default=0)

    class Meta:
        ordering = ['order_index']

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')

class ListeningHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listening_history')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='listening_records')
    listened_at = models.DateTimeField(auto_now_add=True)
    duration_listened = models.IntegerField()  # saniye cinsinden

    class Meta:
        ordering = ['-listened_at'] 