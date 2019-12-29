from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name = 'event')
    year = models.IntegerField()
    month = models.IntegerField()
    date = models.IntegerField()
    time = models.TimeField()
    type = models.CharField(max_length=50)
    interest = models.ManyToManyField(get_user_model(), related_name = 'interested_event')
    participate = models.ManyToManyField(get_user_model(), related_name = 'participated_event')

class Rating(models.Model):
    user = models.ManyToManyField(get_user_model(), related_name = 'rated')
    rating = models.IntegerField(default = 0)
    event = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name = 'rating')
    
class Comment(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name = 'comment')
    comment = models.TextField()
    event = models.ForeignKey('Event', on_delete = models.CASCADE ,related_name = 'comment')