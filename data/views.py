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
from data.permissions import IsOwner

import sqlite3 

def tbl_cnts(request):
    con=sqlite3.connect("./databases/db.sqlite3")
    cur = con.cursor()

    results = cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name")
    tables = [t[0] for t in results.fetchall()]
    user_facing_tables = [t for t in tables if "data_" in t and t != "data_profile"] 

    table_cnts = {}
    for i in tables:
        cur.execute(f"SELECT COUNT(*) FROM {i}")
        table_cnts[i] = cur.fetchone()[0]
    
    metrics = {
        'numtbls' : len(tables), 
        'table_cnts' : table_cnts, 
        'r_tables' : [r for r in tables if r not in user_facing_tables],
        'rt_cnt' : len([r for r in tables if r not in user_facing_tables]),
        'u_tables' : user_facing_tables,
        'ut_cnt' : len(user_facing_tables)
        }
    return render(request, 'data/tblcnts.html', metrics)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    #anyone can create
    #Students can RUD + list only themselves
    #Professors can list all
    #AdminAssistants can update, destroy, retrieve, list all
    
    def get_queryset(self):
        #filter queryset to restrict access scope for the requesting user
        try:
            user = self.request.user
            if user.is_anonymous:
                raise PermissionDenied("Request must have an authenticated user.")
            
            if self.action in ['list', 'retrieve']:
                if user.groups.filter(name__in=["Student"]).exists():
                    prof = Profile.objects.get(user=user)
                    return Student.objects.filter(prof=prof)
            
            #else, for other actions:
            return Student.objects.all()
        
        except Http404:
            pass

    def get_permissions(self):
        if self.action == 'create': #let anyone (unauthenticated) do 'create' action
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['list']:
            self.permission_classes = [permissions.DjangoModelPermissions]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwner | permissions.DjangoModelPermissions] 
        
        return [permission() for permission in self.permission_classes] 
    
    def destroy(self, request, pk=None):
        if pk is not None:
            try:
                s = Student.objects.get(id=pk)
                self.check_object_permissions(self.request, s)
                p = Profile.objects.get(pk=s.prof_id)
                u = User.objects.get(pk=p.user_id)
                u.delete() #-- this cascade deletes Student/Profile too
            except Student.DoesNotExist:
                raise Http404("No Student matches given PK")
        else:
            s = self.get_object() #--checks obj perms too
            u = self.request.user #check perms?
            u.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.DjangoModelPermissions]



class MajorViewSet(viewsets.ModelViewSet):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer
    permission_classes = [permissions.DjangoModelPermissions]



class MinorViewSet(viewsets.ModelViewSet):
    queryset = Minor.objects.all()
    serializer_class = MinorSerializer
    permission_classes = [permissions.DjangoModelPermissions]



class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    #Students can retrieve/list all
    #Professors can UD only themselves, retrieve/list all 
    #AdminAssistants can CRUD + list all

    def get_queryset(self):
        #filter queryset to restrict access scope for the requesting user
        try: 
            user = self.request.user
            if user.is_anonymous:
                raise PermissionDenied("Request must have an authenticated user.")
            
            if self.action in ['list', 'retrieve']:
                # if user.groups.filter(name__in=["Student"]).exists():
                #     raise PermissionDenied("Must be authenticated user w perms.")
                # else: #AdminAssistants
                    # return Professor.objects.all()
                pass
            
            #else, for other actions:
            return Professor.objects.all()

        except Http404:
            pass

    def get_permissions(self):
        if self.action in ['create', 'list']:
            self.permission_classes = [permissions.DjangoModelPermissions]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwner | permissions.DjangoModelPermissions] 
        return [permission() for permission in self.permission_classes] 
    
    def destroy(self, request, pk=None):
        if pk is not None:
            try:
                pf = Professor.objects.get(id=pk)
                self.check_object_permissions(self.request, pf)
                p = Profile.objects.get(pk=pf.prof_id)
                u = User.objects.get(pk=p.user_id)
                u.delete() #-- this cascade deletes Professor/Profile too
            except Professor.DoesNotExist:
                raise Http404("No Professor matches given PK")
        else:
            pf = self.get_object() #--checks obj perms too
            u = self.request.user #check perms?
            u.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



class AdminAssistantViewSet(viewsets.ModelViewSet):
    queryset = AdminAssistant.objects.all()
    serializer_class = AdminAssistantSerializer
    #Professors can retrieve/list all 
    #AdminAssistants can UD only themselves, can create/retrieve/list all 

    def get_queryset(self):
        #filter queryset to restrict access scope for the requesting user
        try: 
            user = self.request.user
            if user.is_anonymous:
                raise PermissionDenied("Request must have an authenticated user.")
            
            if self.action in ['list', 'retrieve']:
                if user.groups.filter(name__in=["Student"]).exists(): #dont allow Students to list/retrieve
                    raise PermissionDenied("Must be authenticated user w perms.")
                return AdminAssistant.objects.all()
            
            #else, for other actions:
            return AdminAssistant.objects.all()

        except Http404:
            pass

    def get_permissions(self):
        if self.action in ['create', 'list']:
            self.permission_classes = [permissions.DjangoModelPermissions]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwner | permissions.DjangoModelPermissions] 
        return [permission() for permission in self.permission_classes] 
    
    def destroy(self, request, pk=None):
        if pk is not None:
            try:
                a = AdminAssistant.objects.get(id=pk)
                self.check_object_permissions(self.request, a)
                p = Profile.objects.get(pk=a.prof_id)
                u = User.objects.get(pk=p.user_id)
                u.delete() #-- this cascade deletes AdminAssistant/Profile too
            except AdminAssistant.DoesNotExist:
                raise Http404("No AdminAssistant matches given PK")
        else:
            a = self.get_object() #--checks obj perms too
            u = self.request.user #check perms?
            u.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



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

