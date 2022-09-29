from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Default Landing Page")

def files(request):
    return render(request, 'BackendDev/files.html',
                {'data': 'test-data'})


