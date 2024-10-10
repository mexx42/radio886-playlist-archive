import requests
from django.http import JsonResponse
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Song

def get_current_song():
    base_url = "https://meta.radio886.at/886/"
    count = 711  # Startwert für count
    
    url = f"{base_url}{count}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler beim Abrufen der Daten: HTTP {response.status_code}")
        return None

def process_song_data(data):
    current_song = next((song for song in data['data'] if song['is_playing']), None)
    if current_song:
        last_song = Song.get_last_song()
        if not last_song or last_song.title != current_song['title'] or last_song.artist != current_song['name']:
            song = Song.objects.create(
                title=current_song['title'],
                artist=current_song['name'],
                timestamp=timezone.now()
            )
            notify_new_song(song)

def notify_new_song(song):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "songs",
        {
            "type": "song_message",
            "message": {
                "type": "new_song",
                "song": {
                    "id": song.id,
                    "title": song.title,
                    "artist": song.artist,
                    "timestamp": song.timestamp.isoformat()
                }
            }
        }
    )
    
def update_current_song(request):
    last_song = Song.get_last_song()
    if last_song:
        play_count = Song.get_play_count(last_song.title, last_song.artist)
        return JsonResponse({
            'status': 'success',
            'song': str(last_song),
            'play_count_last_week': play_count,
        })
    return JsonResponse({'status': 'error', 'message': 'Kein aktueller Song verfügbar'})

def get_song_stats(request):
    title = request.GET.get('title')
    artist = request.GET.get('artist')
    days = int(request.GET.get('days', 7))
    
    if title and artist:
        play_count = Song.get_play_count(title, artist, days)
        return JsonResponse({
            'status': 'success',
            'title': title,
            'artist': artist,
            'play_count': play_count,
            'days': days
        })
    return JsonResponse({'status': 'error', 'message': 'Titel und Künstler sind erforderlich'})

def get_recent_songs(request):
    limit = int(request.GET.get('limit', 10))
    recent_songs = Song.objects.order_by('-timestamp')[:limit]
    songs_data = [{'id': song.id, 'title': song.title, 'artist': song.artist, 'timestamp': song.timestamp} for song in recent_songs]
    return JsonResponse({'status': 'success', 'songs': songs_data})

def get_song_weekly_stats(request):
    title = request.GET.get('title')
    artist = request.GET.get('artist')
    weeks = int(request.GET.get('weeks', 12))
    
    if title and artist:
        weekly_stats = Song.get_weekly_play_count(title, artist, weeks)
        return JsonResponse({
            'status': 'success',
            'title': title,
            'artist': artist,
            'weekly_stats': weekly_stats
        })
    return JsonResponse({'status': 'error', 'message': 'Titel und Künstler sind erforderlich'})