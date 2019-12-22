from django.db import models

# Create your models here.

class event(models.Model):
    title = models.CharField(max_length=100)