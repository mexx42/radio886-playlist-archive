# songtracker/cron.py

from .views import get_current_song, process_song_data

def update_song():
    song_data = get_current_song()
    if song_data:
        process_song_data(song_data)