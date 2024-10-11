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
    def get_weekly_play_count(cls, title=None, artist=None, weeks=12):
        end_date = timezone.now()
        start_date = end_date - timedelta(weeks=weeks)
        query = cls.objects.filter(timestamp__range=(start_date, end_date))
        
        if title:
            query = query.filter(title__icontains=title)
        if artist:
            query = query.filter(artist__icontains=artist)
        
        weekly_counts = query.annotate(
            week=TruncWeek('timestamp')
        ).values('week').annotate(
            count=Count('id')
        ).order_by('week')
        
        print (weekly_counts.count ())
        print (weekly_counts)

        # Fülle fehlende Wochen mit Nullen auf
        all_weeks = {}
        current_week = start_date
        while current_week <= end_date:
            all_weeks[current_week.date()] = 0
            current_week += timedelta(weeks=1)
        
        for entry in weekly_counts:
            all_weeks[entry['week'].date()] = entry['count']
        
        return [{'week': week.isoformat(), 'count': count} for week, count in all_weeks.items()]

    