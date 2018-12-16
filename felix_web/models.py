from django.db import models
from django.contrib.auth import get_user_model

DjangoUser = get_user_model()
# Create your models here.


class User(models.Model):
    phone = models.CharField(max_length=45, primary_key=True)


class Session(models.Model):
    id = models.IntegerField(primary_key=True)
    nomad = models.ForeignKey('User', on_delete=models.CASCADE)
    success = models.NullBooleanField()
    resolved_by_human = models.NullBooleanField()
    created = models.DateTimeField(auto_now_add=True)


class Turn(models.Model):
    nomad = models.ForeignKey('User', on_delete=models.CASCADE)
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE)
    session = models.ForeignKey('Session', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    lat = models.FloatField()
    lon = models.FloatField()
    question = models.TextField()
    answer = models.TextField()
