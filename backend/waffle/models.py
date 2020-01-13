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

class Like(models.Model):
    user = models.ManyToManyField(get_user_model(), related_name = 'likes')
    like = models.IntegerField(default = 0)
    event = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name = 'like')
    
class Posting(models.Model):
    title = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now = True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name = 'posting')
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name = 'posting')
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
