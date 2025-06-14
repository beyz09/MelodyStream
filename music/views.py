from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Song, Artist, Album
from .serializers import SongSerializer, ArtistSerializer
from playlists.models import ListeningHistory # ListeningHistory modelini import ediyoruz
from rest_framework import permissions
from django.shortcuts import get_object_or_404

class SongListAPIView(generics.ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Song.objects.all()
        query = self.request.query_params.get('q', None)
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(artist__icontains=query))
        return queryset

class SongDetailAPIView(generics.RetrieveAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['GET'])
def search_songs(request):
    query = request.GET.get('q', '')
    if query:
        songs = Song.objects.filter(
            Q(song_name__icontains=query) |
            Q(artist__artist_name__icontains=query) |
            Q(album__album_name__icontains=query)
        )
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)
    return Response([])

@api_view(['POST'])
def play_song(request, song_id):
    try:
        song = Song.objects.get(id=song_id)
        song.play_count += 1
        song.save()

        # Dinleme geçmişine ekle
        if request.user.is_authenticated:
            ListeningHistory.objects.create(
                user=request.user,
                song=song,
                duration_listened=0  # Frontend'den gönderilecek
            )

        return Response({'status': 'success'})
    except Song.DoesNotExist:
        return Response({'error': 'Song not found'}, status=404) 