from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from elect.models import Position, Candidate, Vote, AppState, VotedUser
from elect.forms import UserForm

import datetime

@login_required
def index(request):
    # check all application states (application states determine whether some messages and some urls are visible)
    try:
        ie_state = AppState.objects.get(key="is_ended")
        em_state = AppState.objects.get(key="extra_messages")
    except Exception:
        return HttpResponse("[Error 1] Improper app state.")
    
    # otherwise display the index page.
    return render(request, 'index.html',{'page':'index', 'is_ended':ie_state.value, 'is_admin':request.user.is_staff, 'extra_messages':em_state.value})

@login_required
# lists the vote totals.
def listing(request):
    # no more checking of listing_visible because it's admin stuff anyway.
    # check if user is actually admin!
    if request.user.is_staff:
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
    # otherwise don't display stuff
    else:
        return HttpResponse("[Error 4] Not available.")
        
def site_login(request):
    context = {}
    
    # if the user has submitted their credentials
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # redirect URL is acquired via get url
        redirecturl = "/"
        try:
            redirecturl = request.GET['next']
        except Exception:
            pass

        # finally authenticate the person
        user = authenticate(username=username, password=password)
        if user:
            # only log in if the user is active. makes things easy
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(redirecturl)
        context["invalid"] = True
    
    # if the user is redirected via a GET url (the next variable)
    elif request.method == 'GET':
        try:
            nexturl = request.GET.get('next')
        except Exception:
            nexturl = '/'
        context["nexturl"] = nexturl

    # otherwise, display the form, with the form not warning the user
    else:
        context["invalid"] = False
    return render(request, 'login.html', context)

@login_required
def site_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# helper function for checking functionality
def check_not_ended():
    try:
        ie_state = AppState.objects.get(key="is_ended")
    except Exception:
        return HttpResponse("[Error 1] Improper app state.")
    # if is_ended is true, then redirect to home always
    if ie_state.value == 'True':
        return HttpResponseRedirect('/')
    else:
        return None

@login_required
def vote_step1(request):
    # check if election has ended.
    check = check_not_ended()
    if check != None:
        return check
    
    # "page is vote" context is for the nav bar template
    context = {'page':'vote'}
    
    # when the user is already verified via /vote1/"
    if 'vote_hash' in request.session:
        return HttpResponseRedirect('/vote2')
    
    # when the user has submitted the form
    if request.method == 'POST':
        password = request.POST.get('password')
        
        # if the user is authenticated
        if authenticate(username=request.user.username, password=password):
            pass_hash = make_password(password, salt="asin")
            
            # if they already voted, inform them
            if len(VotedUser.objects.filter(key=pass_hash)) != 0:
                context['already_voted'] = True
            
            # otherwise they pass the verification!
            else:
                request.session['vote_hash'] = pass_hash
                return HttpResponseRedirect('/vote2')
        
        # otherwise warn them of non-authentication
        else:
            context['already_voted'] = False
            context['warn'] = True
    
    # display the form otherwise
    else:
        context['already_voted'] = False
    return render(request, 'verify.html', context)
    
@login_required
def vote_step2(request):
    # check if election has ended.
    check = check_not_ended()
    if check:
        return check
        
    # "page is vote" context is for the nav bar template
    context = {'page':'vote'}
    
    # let's check if the vote_hash is in the session because we need it
    try:
        pass_hash = request.session['vote_hash']
    except Exception:
        return HttpResponse("[Error 5] Invalid session.")
    
    # let's check if the user already voted, cheater
    if len(VotedUser.objects.filter(key=pass_hash)) != 0:
        return HttpResponse("[Error 5] Invalid URL.")
    
    positions = Position.objects.all()
    
    # if the user has submitted a form
    if request.method == 'POST':
        
        # check if the form is complete
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
            
            # if the user is not authenticated
            if not authenticate(username=request.user.username, password=password):
                context['invalid_pass'] = True
            
            # otherwise register the vote (party party!)
            else:
                for c in candidate_votes:
                    authstring = make_password(str(c.id)+" "+password, "tuba")
                    Vote.objects.get_or_create(candidate=c, authstring=authstring)
                VotedUser.objects.get_or_create(key=pass_hash)
                del request.session['vote_hash']
                return render(request, 'receive.html', {'page':'receive'})
        
        # otherwise warn user that form is not complete
        except KeyError:
            context['warn'] = True
            
    # when all other conditions fail, print the form.
    context['positions'] = []
    for p in positions:
        candidates =  Candidate.objects.filter(position=p).order_by('id')
        p_prime = {'name':p.name, 'candidates':candidates}
        context['positions'].append(p_prime)
    return render(request, 'vote.html', context)

@login_required
def change(request):
    # check if election has ended.
    check = check_not_ended()
    if check:
        return check
    
    # "page is change" context is for the nav bar template
    context = {'page':'change'}   
    
    # if the user has submitted the change password form
    if request.method == 'POST':
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
        
        # if the user is not auth'd, inform user
        if not authenticate(username=request.user.username, password=password):
            context['wrong_pass'] = True
        
        # if the passwords do not match, inform user
        elif new_password != confirm_new_password:
            context['not_matching'] = True
        
        # if user is dumb and password is empty
        elif new_password == "":
            context['empty'] = True
            
        # otherwise change the password!
        else:
            check_hash = make_password(password, salt="changedna")
            vote_check_hash = make_password(password, salt="asin")
            
            # if user already voted, fail the change password
            if len(VotedUser.objects.filter(key=vote_check_hash)) != 0:
                return render(request, 'receive.html', {'page':'receive', 'already_voted':True})
            
            # if the user already changed passwords (VotedUser database stores this information)
            if len(VotedUser.objects.filter(key=check_hash)) != 0:
                return render(request, 'receive.html', {'page':'receive', 'failed':True})
            
            # otherwise change the password since everything is fine
            else:
                new_check_hash = make_password(new_password, salt="changedna")
                VotedUser.objects.get_or_create(key=new_check_hash)
                new_hash = make_password(new_password)
                edited_user = request.user
                edited_user.password = new_hash
                edited_user.save()
                logout(request)
                return render(request, 'receive.html', {'page':'receive', 'not_a_vote':True})
    return render(request, 'change.html', context)