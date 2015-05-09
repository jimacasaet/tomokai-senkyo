from django.contrib import admin
from works.models import Board, Activity

class BoardAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}

admin.site.register(Board,BoardAdmin)
admin.site.register(Activity)