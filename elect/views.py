from django.shortcuts import render
from django.http import HttpResponse
from elect.models import Position, Candidate, Vote
def index(request):
    return HttpResponse('Election app.')
def registered(request):
    positions = Position.objects.all()
    p_data = []
    for p in positions:
        candidates =  Candidate.objects.filter(position=p)
        c_data = []
        for c in candidates:
            c_prime = {'name':c.name, 'votes':len(Vote.objects.filter(candidate=c))}
            c_data.append(c_prime)
        p_prime = {'name':p.name, 'candidates':c_data}
        p_data.append(p_prime)
    return render(request, 'registered.html', {'positions': p_data})