from django.apps import AppConfig
import threading

class SongtrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'songtracker'

    def ready(self):
        from .views import get_current_song_thread
        
        # Vermeiden Sie doppelte Ausführung im Entwicklungsserver
        if not threading.current_thread().name == 'MainThread':
            return
        
        # Starten Sie das Song-Tracking in einem separaten Thread
        tracking_thread = threading.Thread(target=get_current_song_thread)
        tracking_thread.setDaemon (True)
        tracking_thread.start()