from data.serializers import DepartmentSerializer, MajorSerializer, MinorSerializer
from data.serializers import StudentSerializer, ProfessorSerializer, AdminAssistantSerializer
from data.serializers import CourseSerializer, HighImpactExperienceSerializer, EventSerializer

from data.models import Department, Major, Minor, Profile, Student, Professor, AdminAssistant, Course, HighImpactExperience, Event
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from django.http import Http404
from django.core.exceptions import PermissionDenied
import json

from data.permissions import IsOwner


def api(request):
    return HttpResponse("API Home Page")

# class StudentViewSet(viewsets.ModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#     permission_classes = [permissions.DjangoModelPermissions]
    
#     def create(self, request):#MAY NOT NEED
#         body = json.loads(request.body.decode('utf-8'))
#         # access_token = body.get("access_token")
#         # content = body['content']
#         serializer = StudentSerializer(data=request.data)
    
#     def list(self, request):
#         queryset = Student.objects.all()
#         serializer = StudentSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = Student.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         self.check_object_permissions(request, user)
#         serializer = StudentSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def update(self, request, pk=None):#MAY NEED?
#         queryset = Student.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         self.check_object_permissions(request, user)
#         pass

#     def partial_update(self, request, pk=None):
#         queryset = Student.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = StudentSerializer(queryset, partial=True)
#         return Response(serializer.data)

#     def destroy(self, request, pk=None):
#         try:
#             instance = self.get_object()
#             self.perform_destroy(instance)
#         except Http404:
#             pass
#         return Response(status=status.HTTP_204_NO_CONTENT)



class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def get_queryset(self):
        #filter queryset to only the authenticated user
        try:
            if self.action in ['retrieve', 'update', 'partial_update', 'destroy', 'list']:
                user = self.request.user
                if user.is_anonymous:
                    raise PermissionDenied("Request must have an authenticated user.")
                
                if user.groups.filter(name__in=["Professor", "AdminAssistant"]).exists():
                    return Student.objects.all()
                else:
                    prof = Profile.objects.get(user=user)
                    return Student.objects.filter(prof=prof)
            else: #for create action
                return Student.objects.all()
        except Http404:
            # raise Http404("Fail")
            pass
    
    #https://stackoverflow.com/questions/39392007/django-rest-framework-viewset-permissions-create-without-list
    #https://r-future.github.io/post/custom-permission-for-different-action-in-an-viewset/
    #https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations

    def get_permissions(self):
        if self.action == 'create': #let anyone (unauthenticated) do 'create' action
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy', 'list']:
            self.permission_classes = [IsOwner | permissions.DjangoModelPermissions] 
        
        return [permission() for permission in self.permission_classes] 

    #https://testdriven.io/blog/django-permissions/ -- maybe done in serializer?
    #https://www.webforefront.com/django/permissionchecks.html
    #https://stackoverflow.com/questions/29780060/trying-to-parse-request-body-from-post-in-django
    
    def destroy(self, request, pk=None):
        try:
            if pk is not None:
                s = Student.objects.get(id=pk)
                p = Profile.objects.get(pk=s.prof_id)
                u = User.objects.get(pk=p.user_id)
                u.delete() #-- this cascade deletes Student/Profile too
            else:
                u = self.request.user
                u.delete()
        except Http404:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)



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


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [permissions.AllowAny]


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