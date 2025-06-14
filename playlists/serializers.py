from rest_framework import serializers
from .models import Playlist, PlaylistSong, Favorite, ListeningHistory
from music.serializers import SongSerializer
from authentication.serializers import UserSerializer # Henüz oluşturmadık, birazdan oluşturacağız

class PlaylistSongSerializer(serializers.ModelSerializer):
    song_detail = SongSerializer(source='song', read_only=True)

    class Meta:
        model = PlaylistSong
        fields = '__all__'

class PlaylistSerializer(serializers.ModelSerializer):
    songs = PlaylistSongSerializer(source='playlistsong_set', many=True, read_only=True)
    user_detail = UserSerializer(source='user', read_only=True) # UserSerializer'ı kullanıyoruz

    class Meta:
        model = Playlist
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    song_detail = SongSerializer(source='song', read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Favorite
        fields = '__all__'

class ListeningHistorySerializer(serializers.ModelSerializer):
    song_detail = SongSerializer(source='song', read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = ListeningHistory
        fields = '__all__' 