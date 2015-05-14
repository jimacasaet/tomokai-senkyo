from django.db import models
from django.contrib.auth.models import User

class Position(models.Model):
    name = models.CharField(max_length=128, unique=True)
    def __unicode__(self):
        return self.name
class Candidate(models.Model):
    position = models.ForeignKey(Position)
    name = models.CharField(max_length=128)
    def __unicode__(self):
        return self.name
class Vote(models.Model):
    candidate = models.ForeignKey(Candidate)
    authstring = models.CharField(max_length=128, default="")
    def __unicode__(self):
        return self.authstring
class AppState(models.Model):
    key = models.CharField(max_length=128, unique=True)
    value = models.CharField(max_length=128)
    def __unicode__(self):
        return self.key
class VotedUser(models.Model):
    key = models.CharField(max_length=128)
    def __unicode__(self):
        return self.key