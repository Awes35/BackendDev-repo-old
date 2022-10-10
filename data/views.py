from django.http import HttpResponse
from django.shortcuts import render
from data.serializers import SerializerCourses, SerializerDepartments, SerializerFaculty, SerializerHighImpactExperiences, SerializerMajors, SerializerMinors, SerializerStudents
from data.models import Courses, Departments, Faculty, HighImpactExperiences, Majors, Minors, Students
from rest_framework import viewsets, permissions

def api(request):
    return HttpResponse("API Home Page")

class HighImpactExperiencesViewSet(viewsets.ModelViewSet):
    queryset = HighImpactExperiences.objects.all()
    serializer_class = SerializerHighImpactExperiences
    permission_classes = [permissions.AllowAny]

class DepartmentsViewSet(viewsets.ModelViewSet):
    queryset = Departments.objects.all()
    serializer_class = SerializerDepartments
    permission_classes = [permissions.AllowAny]

class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = SerializerFaculty
    permission_classes = [permissions.AllowAny]

class CoursesViewSet(viewsets.ModelViewSet):
    queryset = Courses.objects.all()
    serializer_class = SerializerCourses
    permission_classes = [permissions.AllowAny]

class MajorsViewSet(viewsets.ModelViewSet):
    queryset = Majors.objects.all()
    serializer_class = SerializerMajors
    permission_classes = [permissions.AllowAny]

class MinorsViewSet(viewsets.ModelViewSet):
    queryset = Minors.objects.all()
    serializer_class = SerializerMinors
    permission_classes = [permissions.AllowAny]

class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = SerializerStudents
    permission_classes = [permissions.AllowAny]
