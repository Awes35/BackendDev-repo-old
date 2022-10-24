from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login

def index(request):
    return HttpResponse("Default Landing Page")

def files(request):
    return render(request, 'BackendDev/files.html',
                {'data': 'test-data'})

def auth(request):
    nm = request.POST['username']
    pw = request.POST['password']
    user = authenticate(request, username=nm, password=pw)
    if user is not None:
        login(request, user)
        #redirect to success page
    else:
        #return an 'invalid login' message
        pass
