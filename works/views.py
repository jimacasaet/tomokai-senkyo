from django.shortcuts import render
from django.http import HttpResponse
from works.models import Board, Activity

# Create your views here.
def index(request):
    board_list = Board.objects.all()
    output = []
    for i in range(len(board_list)):
        board = board_list[i]
        activities = Activity.objects.filter(board=board)
        output.append({'board':board,'activities':activities})
    print output
    context_dict = {'image':'mweeface.jpg',
        'list':output,
        'text':'Works',
        'column_param':len(board_list)+1, }
    return render(request,'works/temp.html', context_dict)

def about(request):
    context_dict = {'image':'pepe.gif',
        'text':'About This Site',
        'about':'This site is a project greenlighted in Trello. It is meant to be used, hopefully.',        
        'board_number':0, }
    return render(request,'works/temp.html', context_dict)

def board(request, board_name_slug):
    board_obj = Board.objects.get(slug=board_name_slug)
    board_obj.views += 1
    board_obj.save()
    activities_obj = Activity.objects.filter(board=board_obj)
    context_dict = {'image':'mweeface.jpg',
        'board':board_obj,
        'activities':activities_obj}
    return render(request,'works/board.html', context_dict)