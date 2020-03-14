from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    content = models.TextField()
    upload_date = models.DateTimeField(auto_now = True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name = 'event')
    date = models.DateField(db_index=True)
    time = models.TimeField()
    event_type = models.CharField(max_length=50)
    interest = models.ManyToManyField(get_user_model(), related_name = 'interested_event')
    participate = models.ManyToManyField(get_user_model(), related_name = 'participated_event')
    like = models.ManyToManyField(get_user_model(), related_name = 'like_event')
    
class Posting(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    upload_date = models.DateTimeField(auto_now = True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name = 'posting')
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name = 'posting')
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')

class EventComment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name = 'event_comment')
    event = models.ForeignKey(Event, on_delete = models.CASCADE, related_name = 'comment', db_index=True)
    upload_date = models.DateTimeField(auto_now = True)

class QnA(models.Model):
    question = models.TextField()
    answer = models.TextField()
    completed = models.BooleanField(null=, blank=True)
    question_author = models.ForeignKey(get_user_model(), on_delete = models.CASCADE, related_name = 'question')
    answer_author = models.ForeignKey(get_user_model(), on_delete = models.CASCADE, related_name = 'answer', null = True, blank=True)
    event = models.ForeignKey(Event, on_delete = models.CASCADE, related_name = 'QnA', db_index=True)
    upload_date = models.DateTimeField(auto_now = True)