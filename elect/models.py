from django.db import models

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
    authstring = models.CharField(max_length=128)
    def __unicode__(self):
        return self.authstring