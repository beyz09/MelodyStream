from django.shortcuts import render
from music.models import Song
from django.db.models import Q

# Create your views here.

def home(request):
    query = request.GET.get('q')
    songs = Song.objects.all()
    if query:
        songs = songs.filter(Q(title__icontains=query) | Q(artist__icontains=query))
    return render(request, 'home.html', {'songs': songs})
