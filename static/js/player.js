// static/js/player.js
class MusicPlayer {
    constructor() {
        this.audio = new Audio();
        this.currentSong = null;
        this.isPlaying = false;
        this.playlist = [];
        this.currentIndex = 0;
        
        this.initializePlayer();
        this.fetchAndRenderSongs(); // Sayfa yüklendiğinde şarkıları getir
    }
    
    initializePlayer() {
        // Player controls
        document.getElementById('play-btn').addEventListener('click', () => {
            this.togglePlay();
        });
        
        document.getElementById('prev-btn').addEventListener('click', () => {
            this.previousSong();
        });
        
        document.getElementById('next-btn').addEventListener('click', () => {
            this.nextSong();
        });
        
        // Volume control
        document.getElementById('volume-slider').addEventListener('input', (e) => {
            this.audio.volume = e.target.value / 100;
        });
        
        // Progress bar
        this.audio.addEventListener('timeupdate', () => {
            this.updateProgress();
        });
        
        this.audio.addEventListener('ended', () => {
            this.nextSong();
        });
    }
    
    async playSong(songId) {
        try {
            const response = await fetch(`/api/music/songs/${songId}/`); // API URL'sini güncelledik
            const song = await response.json();
            
            this.currentSong = song;
            this.audio.src = song.audio_file;
            this.audio.play();
            this.isPlaying = true;
            
            this.updateUI();
            this.recordPlay(songId);
            
        } catch (error) {
            console.error('Error playing song:', error);
        }
    }
    
    togglePlay() {
        if (this.isPlaying) {
            this.audio.pause();
            this.isPlaying = false;
            document.getElementById('play-btn').innerHTML = '<i class="fas fa-play"></i>';
        } else {
            this.audio.play();
            this.isPlaying = true;
            document.getElementById('play-btn').innerHTML = '<i class="fas fa-pause"></i>';
        }
    }
    
    updateUI() {
        if (this.currentSong) {
            document.getElementById('current-song').textContent = this.currentSong.song_name;
            document.getElementById('current-artist').textContent = this.currentSong.artist_name;
            document.getElementById('current-cover').src = this.currentSong.album_cover || '/static/img/default-cover.jpg'; // Varsayılan kapak resmi
            document.getElementById('play-btn').innerHTML = '<i class="fas fa-pause"></i>';
        }
    }
    
    updateProgress() {
        if (this.audio.duration) {
            const progress = (this.audio.currentTime / this.audio.duration) * 100;
            document.getElementById('progress-bar').style.width = progress + '%';
        }
    }
    
    async recordPlay(songId) {
        // CSRF token'ını almak için bir meta etiketi oluşturulduğunu varsayıyoruz.
        // Veya frontend tarafında bir CSRF token yönetimi implemente edilebilir.
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; // base.html'e eklenecek

        await fetch(`/api/music/songs/${songId}/play/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                // duration_listened buraya eklenecek, bu örnekte 0 olarak bırakıldı.
                // Gerçek bir uygulamada, oynatma durdurulduğunda veya şarkı bittiğinde bu değer gönderilir.
                duration_listened: 0 
            })
        });
    }

    async fetchAndRenderSongs() {
        try {
            const urlParams = new URLSearchParams(window.location.search);
            const query = urlParams.get('q');
            let apiUrl = '/api/music/songs/';
            if (query) {
                apiUrl += `?q=${query}`;
            }
            const response = await fetch(apiUrl);
            const songs = await response.json();
            this.playlist = songs; // Şarkıları çalma listesine ekle
            this.renderSongs(songs);
        } catch (error) {
            console.error('Error fetching songs:', error);
        }
    }

    renderSongs(songs) {
        const songListDiv = document.getElementById('song-list');
        songListDiv.innerHTML = ''; // Önceki içeriği temizle

        songs.forEach(song => {
            const songCard = `
                <div class="col mb-4">
                    <div class="card bg-dark text-white h-100">
                        <img src="${song.album_cover || '/static/img/default-cover.jpg'}" class="card-img-top" alt="${song.album_name} Cover">
                        <div class="card-body">
                            <h5 class="card-title">${song.song_name}</h5>
                            <p class="card-text text-muted">${song.artist_name}</p>
                            <button class="btn btn-primary play-song-btn" data-song-id="${song.id}">
                                <i class="fas fa-play"></i> Çal
                            </button>
                        </div>
                    </div>
                </div>
            `;
            songListDiv.innerHTML += songCard;
        });

        // Yeni eklenen butonlara event listener ekle
        document.querySelectorAll('.play-song-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const songId = this.dataset.songId;
                player.playSong(songId);
            });
        });
    }

    previousSong() {
        if (this.playlist.length === 0) return;
        this.currentIndex = (this.currentIndex - 1 + this.playlist.length) % this.playlist.length;
        this.playSong(this.playlist[this.currentIndex].id);
    }

    nextSong() {
        if (this.playlist.length === 0) return;
        this.currentIndex = (this.currentIndex + 1) % this.playlist.length;
        this.playSong(this.playlist[this.currentIndex].id);
    }
}

// Initialize player
const player = new MusicPlayer();

// Song list click handlers - Bu kısım artık MusicPlayer sınıfı içinde yönetiliyor
// document.addEventListener('DOMContentLoaded', function() {
//     document.querySelectorAll('.play-song-btn').forEach(btn => {
//         btn.addEventListener('click', function() {
//             const songId = this.dataset.songId;
//             player.playSong(songId);
//         });
//     });
// }); 