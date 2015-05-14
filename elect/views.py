from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from elect.models import Position, Candidate, Vote, AppState, VotedUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from elect.forms import UserForm
import datetime
@login_required

def index(request):
    try:
        em_state = AppState.objects.get(key="extra_messages")
        lv_state = AppState.objects.get(key="listing_visible")
        rm_state = AppState.objects.get(key="remove_message")
    except Exception:
        return HttpResponse("[Error 1] Improper app state.")
    return render(request, 'index.html',{'page':'index', 'extra_messages':em_state.value, 'listing_visible':lv_state.value, 'remove_message':rm_state.value})

@login_required
def listing(request):
    try:
        state = AppState.objects.get(key="listing_visible")
    except Exception:
        return HttpResponse("[Error 2] Improper app state.")
    if state.value == "False":
        return HttpResponse("[Error 3] Not available.")
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
    return render(request, 'listing.html', {'positions': p_data, 'page':'listing'})

def site_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        redirecturl = "/"
        try:
            redirecturl = request.GET['next']
        except Exception:
            pass
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(redirecturl)
        context["invalid"] = True
    elif request.method == 'GET':
        try:
            nexturl = request.GET.get('next')
        except Exception:
            nexturl = '/'
        context["nexturl"] = nexturl
    else:
        context["invalid"] = False
    return render(request, 'login.html', context)

@login_required
def site_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def vote_step1(request):
    context = {'page':'vote'}
    if 'vote_hash' in request.session:
        return HttpResponseRedirect('/vote2')
    if request.method == 'POST':
        password = request.POST.get('password')
        if authenticate(username=request.user.username, password=password):
            pass_hash = make_password(password, salt="asin")
            if len(VotedUser.objects.filter(key=pass_hash)) != 0:
                context['verified'] = True
            else:
                request.session['vote_hash'] = pass_hash
                return HttpResponseRedirect('/vote2')
        else:
            context['verified'] = False
            context['warn'] = True
    else:
        context['verified'] = False
    return render(request, 'verify.html', context)
    
@login_required
def vote_step2(request):
    try:
        pass_hash = request.session['vote_hash']
    except Exception:
        return HttpResponse("[Error 5] Invalid session.")
    if len(VotedUser.objects.filter(key=pass_hash)) != 0:
        return HttpResponse("[Error 5] Invalid URL.")
    context = {'page':'vote'}
    positions = Position.objects.all()
    if request.method == 'POST':
        try:
            data = []
            candidate_votes = []
            for p in positions:                
                votename = request.POST['choice'+p.name]
                voteid = int(votename)
                candidate = Candidate.objects.get(id=voteid)
                candidate_votes.append(candidate)
                data.append(votename)
            password = request.POST['password']
            for c in candidate_votes:
                authstring = make_password(c.name+" "+password, "tuba")
                Vote.objects.get_or_create(candidate=c, authstring=authstring)
            VotedUser.objects.get_or_create(key=pass_hash)
            del request.session['vote_hash']
            return render(request, 'receive.html', {'page':'receive'})
        except KeyError:
            context['warn'] = True
    context['positions'] = []
    for p in positions:
        candidates =  Candidate.objects.filter(position=p)
        p_prime = {'name':p.name, 'candidates':candidates}
        context['positions'].append(p_prime)
    return render(request, 'vote.html', context)

def change(request):
    context = {'page':'change'}
    if request.method == 'POST':
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
        if  new_password != confirm_new_password:
            context['not_matching'] = True
        else:
            return render(request, 'receive.html', {'page':'receive', 'not_a_vote':True})
    return render(request, 'change.html', context)