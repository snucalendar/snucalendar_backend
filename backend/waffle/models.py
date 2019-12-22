from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'event')
    year = models.IntegerField()
    month = models.IntegerField()
    date = models.IntegerField()
    time = models.TimeField()
    type = models.CharField(max_length=50)
    interest = models.ManyToManyField(User, related_name = 'interested_event')
    participate = models.ManyToManyField(User, related_name = 'participated_event')
class Rating(models.Model):
    user = models.ManyToManyField(User, related_name = 'rated')
    rating = models.IntegerField(default = 0)
    event = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'rating')
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'comment')
    comment = models.TextField()
    event = models.ForeignKey('Event', on_delete = models.CASCADE ,related_name = 'comment')