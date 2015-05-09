import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finish.settings')

import django
django.setup()
from works.models import Board, Activity
boards_input = [["Anime",["Hitsugi no Chaika"]],["Visual Novels",["Narcissu"]],["Games",[]]]
for board_input in boards_input:
    b = Board.objects.get_or_create(title=board_input[0])[0]
    for activity_input in board_input[1]:
        a = Activity.objects.get_or_create(board=b, title=activity_input, progress=0)[0]