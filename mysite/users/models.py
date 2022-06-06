from django.utils import timezone

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=50)
    ifLogged = models.BooleanField(default=False)
    token = models.CharField(max_length=500, null=True, default="")

    def __str__(self): 
        return self.username

class Message(models.Model):
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    created = models.DateTimeField(default=timezone.now)
    isRead = models.BooleanField(default=False)

    def __str__(self): 
        return self.subject
