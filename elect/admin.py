from django.contrib import admin
from elect.models import Position, Candidate, Vote

admin.site.register(Position)
admin.site.register(Candidate)
admin.site.register(Vote)