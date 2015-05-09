from django.db import models
from django.template.defaultfilters import slugify

class Board(models.Model):
    title = models.CharField(max_length=140, unique=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Board,self).save(*args, **kwargs)
    def __unicode__(self):
        return self.title
class Activity(models.Model):
    board = models.ForeignKey(Board)
    title = models.CharField(max_length=140)
    progress = models.IntegerField(default=0)
    def __unicode__(self):
        return self.title
