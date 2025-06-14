from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('music/', include('music.urls')),
    path('playlists/', include('playlists.urls')),
] 