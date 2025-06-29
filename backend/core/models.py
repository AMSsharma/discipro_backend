import datetime
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User 

class UserProfile(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    inspirations=models.JSONField(default=list, blank=True)
    todays_score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    def __str__(self):
        return self.name
    
class UserScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    overall_score = models.IntegerField(default=0)
    daily_score = models.IntegerField(default=0)
    weekly_score = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    last_score = models.IntegerField(default=0)  # to track score before the latest update
    last_updated_date = models.DateField(default=datetime.date.today)
    def __str__(self):
        return f"{self.user.username} - {self.overall_score}"

class Tasks(models.Model):
    title = models.CharField(max_length=100)
    duration= models.DurationField(default=timedelta())  # Default duration is 1 day
    description = models.TextField()
    pdf = models.FileField(upload_to='tasks/pdfs/', blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    iscomplete = models.BooleanField(default=False)
    inprogress = models.BooleanField(default=False)
    isDone = models.BooleanField(default=False)

    def __str__(self):
        return self.title
from django.contrib.auth.models import User
from django.db import models

# class Score(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     points = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username}: {self.points} @ {self.created_at}"

