from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

class IsOwner(permissions.BasePermission):

    authenticated_users_only = True

    def has_permission(self, request, view):
        if request.method in ['POST']: 
            return False #no owners for CREATE action
        
        # if not request.user: #or (
        #    not request.user.is_authenticated and self.authenticated_users_only):
            # return False
        
        return request.user and request.user.is_authenticated #return True
    
    def has_object_permission(self, request, view, obj):
        print(f"\nrequest user: {request.user}")
        print(f"obj-prof-user: {obj.prof.user}\n")
        # return super().has_object_permission(request, view, obj)
        return obj.prof.user == request.user

