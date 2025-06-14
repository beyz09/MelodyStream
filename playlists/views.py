from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Playlist, PlaylistSong, Favorite, ListeningHistory
from music.models import Song
from .serializers import PlaylistSerializer, PlaylistSongSerializer, FavoriteSerializer

class PlaylistCreateView(generics.CreateAPIView):
    serializer_class = PlaylistSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PlaylistListView(generics.ListAPIView):
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)

class PlaylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def get_object(self):
        obj = get_object_or_404(Playlist, pk=self.kwargs['pk'], user=self.request.user)
        return obj

@api_view(['POST'])
def add_to_favorites(request, song_id):
    try:
        song = Song.objects.get(id=song_id)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            song=song
        )
        if created:
            return Response({'status': 'added'}, status=status.HTTP_201_CREATED)
        else:
            favorite.delete()
            return Response({'status': 'removed'}, status=status.HTTP_200_OK)
    except Song.DoesNotExist:
        return Response({'error': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_song_to_playlist(request, playlist_id, song_id):
    try:
        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        song = get_object_or_404(Song, id=song_id)
        
        playlist_song, created = PlaylistSong.objects.get_or_create(
            playlist=playlist,
            song=song
        )
        if created:
            return Response({'status': 'song added to playlist'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'song already in playlist'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 