from django.urls import path
from . import views

urlpatterns = [
    path('update-song/', views.update_current_song, name='update_song'),
    path('song-stats/', views.get_song_stats, name='song_stats'),
    path('recent-songs/', views.get_recent_songs, name='recent_songs'),
    path('song-weekly-stats/', views.get_song_weekly_stats, name='song_weekly_stats'),
]