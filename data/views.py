from django.http import HttpResponse
from django.shortcuts import render


def api(request):
    return HttpResponse("API Home Page")

