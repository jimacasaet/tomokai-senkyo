from django.shortcuts import render, get_object_or_404
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

def vote(request):
    positions = Position.objects.all()
    p_data = []
    for p in positions:
        candidates =  Candidate.objects.filter(position=p)
        p_prime = {'name':p.name, 'candidates':candidates}
        p_data.append(p_prime)
    return render(request, 'vote.html', {'positions': p_data})
    
def receive(request):
    positions = Position.objects.all()
    data = []
    for p in positions:
        try:
            votename = request.POST['choice'+p.name]
            voteid = int(votename)
            candidate = Candidate.objects.get(id=voteid)
            Vote.objects.get_or_create(candidate=candidate, authstring="DRIL")
        except KeyError:
            votename = "None"
        data.append(votename)
    return render(request, 'receive.html', {'result':data})