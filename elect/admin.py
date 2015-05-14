from django.contrib import admin
from elect.models import Position, Candidate, Vote, AppState, VotedUser
from django.contrib.auth.models import User

admin.site.register(Position)
admin.site.register(Candidate)
admin.site.register(Vote)
admin.site.register(AppState)
admin.site.register(VotedUser)