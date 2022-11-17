from django.http import HttpResponse
from django.shortcuts import render
from data.serializers import DepartmentSerializer, MajorSerializer, MinorSerializer
from data.serializers import StudentSerializer, ProfessorSerializer, AdminAssistantSerializer
from data.serializers import CourseSerializer, HighImpactExperienceSerializer, EventSerializer
from data.models import Department, Major, Minor, Student, Professor, AdminAssistant, Course, HighImpactExperience, Event
from rest_framework import viewsets, permissions

def api(request):
    return HttpResponse("API Home Page")

class StudentViewSet(viewsets.ViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.AllowAny]


class MajorViewSet(viewsets.ModelViewSet):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer
    permission_classes = [permissions.AllowAny]


class MinorViewSet(viewsets.ModelViewSet):
    queryset = Minor.objects.all()
    serializer_class = MinorSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class AdminAssistantViewSet(viewsets.ModelViewSet):
    queryset = AdminAssistant.objects.all()
    serializer_class = AdminAssistantSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class HighImpactExperienceViewSet(viewsets.ModelViewSet):
    queryset = HighImpactExperience.objects.all()
    serializer_class = HighImpactExperienceSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.DjangoModelPermissions] 