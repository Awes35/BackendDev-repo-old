from django.http import HttpResponse
from django.shortcuts import render
from data.models import HighImpactExperience #temp
from django.core import serializers #temp
from data.serializers import HighImpactExperienceSerializer
import json
from django.contrib.auth import authenticate, login

def index(request):
    return HttpResponse("Default Landing Page")

def files(request):
    return render(request, 'BackendDev/files.html',
                {'data': 'sample-data'})

def HIEs_display(request): #temp - MVT
    data = HighImpactExperience.objects.all()
    return render(request, 'data/hie.html', {'hie_entries': data})


def HIEs_raw(request): #temp - DRF
    data = HighImpactExperience.objects.all()
    serializer = HighImpactExperienceSerializer(data, many=True)
    json_data = json.dumps(serializer.data)
    return HttpResponse(json_data, content_type='application/json')


# def HIEs_raw(request): #temp
#     hie_entries = HighImpactExperience.objects.all()
#     data = serializers.serialize('json', hie_entries)

#     return HttpResponse(data, content_type='application/json')


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
