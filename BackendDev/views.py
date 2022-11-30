from django.http import HttpResponse
from django.shortcuts import render
from data.models import HighImpactExperience #temp
from django.core import serializers #temp
from data.serializers import HighImpactExperienceSerializer #temp
import json
from django.contrib.auth import authenticate, login

from django.urls import URLPattern, URLResolver
from django.conf import settings
from BackendDev.settings import RESTRICTED_PATHS

def list_urls(lis, acc=None):
    if acc is None:
        acc = []
    if not lis:
        return
    l = lis[0]
    if isinstance(l, URLPattern):
        yield acc + [str(l.pattern)]
    elif isinstance(l, URLResolver):
        yield from list_urls(l.url_patterns, acc + [str(l.pattern)])
    yield from list_urls(lis[1:], acc)


def urlpaths(request):
    urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])
    path_lst = ["-- Server Endpoint Paths --"]
    for p in list_urls(urlconf.urlpatterns):
        # print(f"\nBefore: {p}")
        skip=False
        for rp in RESTRICTED_PATHS:
            if rp in str(p):
                skip=True
        if skip:
            # print(f"SKIPPING <{p}>")
            continue

        p = "".join(p)
        
        p = str(p).replace("(?P<pk>[^/.]+)", "<int:pk>")
        p = str(p).replace("^", "")
        p = str(p).replace("$", "")
        # print(f"After: {p}")

        path_lst = path_lst + [p]
    
    return HttpResponse("\n".join(path_lst), content_type="text/plain")


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
