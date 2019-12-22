from django.db import models
from django.contrib.auth import User

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'event')
    date = models.DateField()
    time = models.TimeField()
    type = models.CharField(max_length=50)
    participate = models.ManyToManyField(User, related_name = 'participated_event')
class Rating(models.Model):
    user = models.ManyToManyField(User)
    rating = models.IntegerField()
    event = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'rating')
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'comment')
    comment = models.TextField()
    event = models.ManyToManyField('Event', related_name = 'comment')