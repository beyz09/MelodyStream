from rest_framework import serializers
from .models import Artist, Album, Song

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.artist_name', read_only=True)

    class Meta:
        model = Album
        fields = '__all__'

class SongSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.artist_name', read_only=True)
    album_name = serializers.CharField(source='album.album_name', read_only=True)
    album_cover = serializers.ImageField(source='album.cover_image', read_only=True)

    class Meta:
        model = Song
        fields = '__all__' 