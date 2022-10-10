from django.http import HttpResponse
from django.shortcuts import render
from data.serializers import SerializerHighImpactExperiences
from data.models import HighImpactExperiences
from rest_framework import viewsets, permissions

def api(request):
    return HttpResponse("API Home Page")

class HIEViewSet(viewsets.ModelViewSet):
    queryset = HighImpactExperiences.objects.all()
    serializer_class = SerializerHighImpactExperiences
    permission_classes = [permissions.AllowAny]
