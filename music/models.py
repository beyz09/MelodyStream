from django.db import models
from authentication.models import User

class Artist(models.Model):
    artist_name = models.CharField(max_length=100)
    biography = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    genre = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='artists/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.artist_name

class Album(models.Model):
    album_name = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    release_date = models.DateField()
    genre = models.CharField(max_length=50, null=True, blank=True)
    cover_image = models.ImageField(upload_to='albums/', null=True, blank=True)
    total_tracks = models.IntegerField(default=0)
    duration_minutes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.album_name} - {self.artist.artist_name}"

class Song(models.Model):
    song_name = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    duration_seconds = models.IntegerField()
    audio_file = models.FileField(upload_to='songs/')
    lyrics = models.TextField(null=True, blank=True)
    play_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.song_name} - {self.artist.artist_name}" 