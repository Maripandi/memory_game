from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class GameUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usertype = models.CharField(max_length=15)

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    started_at = models.DateField(auto_now_add=True)
    ended_at = models.DateField(null=True)
    is_completed = models.BooleanField()
    last_state = models.CharField(max_length=50,null=True)
    def __str__(self):
        return f'{self.user} -> Game'

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return f'{self.user} -> score'

class Card(models.Model):
    value = models.CharField( max_length=15)
    is_matched = models.BooleanField()
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.value
    

