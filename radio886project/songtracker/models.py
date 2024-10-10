from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncWeek

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.artist} - {self.title} (Gespielt am {self.timestamp})"

    @classmethod
    def get_play_count(cls, title, artist, days=7):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        return cls.objects.filter(
            title=title,
            artist=artist,
            timestamp__range=(start_date, end_date)
        ).count()

    @classmethod
    def get_last_song(cls):
        return cls.objects.order_by('-timestamp').first()

    @classmethod
    def get_weekly_play_count(cls, title, artist, weeks=12):
        end_date = timezone.now()
        start_date = end_date - timedelta(weeks=weeks)
        weekly_counts = cls.objects.filter(
            title=title,
            artist=artist,
            timestamp__range=(start_date, end_date)
        ).annotate(
            week=TruncWeek('timestamp')
        ).values('week').annotate(
            count=Count('id')
        ).order_by('week')
        return list(weekly_counts)