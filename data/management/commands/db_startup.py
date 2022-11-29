# from this import d
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group, Permission

# from django.contrib.auth.backends import ModelBackend 
from django.contrib.contenttypes.models import ContentType
from data.models import (
    Department,
    Major,
    Minor,
    Student,
    Professor,
    AdminAssistant,
    Course,
    HighImpactExperience,
    Event,
    Profile
)

#start: (with no databases and no migrations)
#-python manage.py makemigrations data
#-python manage.py migrate
#call command via: python manage.py db_startup

GROUPS = ['Students', 'Professors', 'AdminAssistants']

class Command(BaseCommand):
    help = 'Initialize databases with authenticated users for access'

    def handle(self, *args, **kwargs):
        try:
            #create superuser
            su = User.objects.create_superuser(username="backend", password="xu261backend_su")

            #CREATE GROUPS
            # https://testdriven.io/blog/django-permissions/
            # https://stackoverflow.com/questions/22250352/programmatically-create-a-django-group-with-permissions
            
            stud_group, created = Group.objects.get_or_create(name="Student")
            prof_group, created = Group.objects.get_or_create(name="Professor")
            aa_group, created = Group.objects.get_or_create(name="AdminAssistant")

            #post (create) -- requires add_
            #put, patch (updates) -- requires change_
            #delete (destroy) -- requires delete_
            #get (list, retrieve) -- requires view_

            #-Student model
            content_type = ContentType.objects.get_for_model(Student)
            post_perm = Permission.objects.filter(content_type=content_type)
            print(f"Student Perms:\n{[perm.codename for perm in post_perm]}\n") #-- ['add_student', 'change_student', 'delete_student', 'view_student']
            #anyone can create
            #Students can RUD + list only themselves
            #Professors can list all
            #AdminAssistants can update, destroy, retrieve, list all
            for perm in post_perm:
                if perm.codename == "add_student":
                    stud_group.permissions.add(perm)
                    prof_group.permissions.add(perm)
                    aa_group.permissions.add(perm)
                elif perm.codename == "view_student":
                    prof_group.permissions.add(perm)
                    aa_group.permissions.add(perm)
                else:
                    aa_group.permissions.add(perm)

            #-Professor model
            content_type = ContentType.objects.get_for_model(Professor)
            post_perm = Permission.objects.filter(content_type=content_type)
            print(f"Prof Perms:\n{[perm.codename for perm in post_perm]}\n") #-- ['add_professor', 'change_professor', 'delete_professor', 'view_professor']
            #Students can retrieve/list all
            #Professors can UD only themselves, retrieve/list all 
            #AdminAssistants can CRUD + list all
            for perm in post_perm:
                if perm.codename == "view_professor":
                    stud_group.permissions.add(perm)
                    prof_group.permissions.add(perm)
                    aa_group.permissions.add(perm)
                else:
                    aa_group.permissions.add(perm)
            
            #-AdminAssistant model
            content_type = ContentType.objects.get_for_model(AdminAssistant)
            post_perm = Permission.objects.filter(content_type=content_type)
            print(f"AdminAssistant Perms:\n{[perm.codename for perm in post_perm]}\n") #-- ['add_adminassistant', 'change_adminassistant', 'delete_adminassistant', 'view_adminassistant']
            #Professors can retrieve/list all 
            #AdminAssistants can UD only themselves, can create/retrieve/list all 
            for perm in post_perm:
                if perm.codename == "add_adminassistant":
                    aa_group.permissions.add(perm)
                elif perm.codename == "view_adminassistant":
                    aa_group.permissions.add(perm)
                    prof_group.permissions.add(perm)

            #-Department model
            content_type = ContentType.objects.get_for_model(Department)
            post_perm = Permission.objects.filter(content_type=content_type)
            print(f"Department Perms:\n{[perm.codename for perm in post_perm]}\n") #-- ['add_department', 'change_department', 'delete_department', 'view_department']
            #superuser will create/update/delete
            for perm in post_perm:
                if perm.codename == "view_department":
                    stud_group.permissions.add(perm)
                    prof_group.permissions.add(perm)
                    aa_group.permissions.add(perm)
            
            #-Major model
            content_type = ContentType.objects.get_for_model(Major)
            post_perm = Permission.objects.filter(content_type=content_type)
            print(f"Major Perms:\n{[perm.codename for perm in post_perm]}\n") #-- ['add_major', 'change_major', 'delete_major', 'view_major']
            #AdminAssistant will create/change/delete
            #any can list/retrieve
            for perm in post_perm:
                if perm.codename == "view_major":
                    stud_group.permissions.add(perm)
                    prof_group.permissions.add(perm)
                    aa_group.permissions.add(perm)
                else:
                    aa_group.permissions.add(perm)

            #-Minor model
            content_type = ContentType.objects.get_for_model(Minor)
            post_perm = Permission.objects.filter(content_type=content_type)
            print(f"Minor Perms:\n{[perm.codename for perm in post_perm]}\n") #-- ['add_minor', 'change_minor', 'delete_minor', 'view_minor']
            #AdminAssistant will create/change/delete
            #any can list/retrieve
            for perm in post_perm:
                if perm.codename == "view_minor":
                    stud_group.permissions.add(perm)
                    prof_group.permissions.add(perm)
                    aa_group.permissions.add(perm)
                else:
                    aa_group.permissions.add(perm)

            #-Course model
            content_type = ContentType.objects.get_for_model(Course)
            post_perm = Permission.objects.filter(content_type=content_type)
            print(f"Course Perms:\n{[perm.codename for perm in post_perm]}\n") #-- ['add_course', 'change_course', 'delete_course', 'view_course']
            #Professor or AdminAssistant will create/change/delete
            #any can list/retrieve
            for perm in post_perm:
                if perm.codename == "view_course":
                    stud_group.permissions.add(perm)
                    prof_group.permissions.add(perm)
                    aa_group.permissions.add(perm)
                else:
                    aa_group.permissions.add(perm)
                    prof_group.permissions.add(perm)

            #-HighImpactExperience model
            content_type = ContentType.objects.get_for_model(HighImpactExperience)
            post_perm = Permission.objects.filter(content_type=content_type)
            print(f"HIE Perms:\n{[perm.codename for perm in post_perm]}\n") #-- ['add_HighImpactExperience', 'change_HighImpactExperience', 'delete_HighImpactExperience', 'view_HighImpactExperience']
            #Professor or AdminAssistant will create/change/delete
            #any can list/retrieve
            for perm in post_perm:
                if perm.codename == "view_HighImpactExperience":
                    stud_group.permissions.add(perm)
                    prof_group.permissions.add(perm)
                    aa_group.permissions.add(perm)
                else:
                    aa_group.permissions.add(perm)
                    prof_group.permissions.add(perm)
            
            #-Event model
            content_type = ContentType.objects.get_for_model(Event)
            post_perm = Permission.objects.filter(content_type=content_type)
            print(f"Event Perms:\n{[perm.codename for perm in post_perm]}\n") #-- ['add_event', 'change_event', 'delete_event', 'view_event']
            #Professor or AdminAssistant will create/change/delete
            #any can list/retrieve
            for perm in post_perm:
                if perm.codename == "view_event":
                    stud_group.permissions.add(perm)
                    prof_group.permissions.add(perm)
                    aa_group.permissions.add(perm)
                else:
                    aa_group.permissions.add(perm)
                    prof_group.permissions.add(perm)
            

            #INITIALIZE DEPARTMENTS TABLE
            d = Department.objects.create(name='Mathematics')
            Department.objects.create(name='Biology')
            Department.objects.create(name='Psychology')
            d1 = Department.objects.create(name='Computer Science')
            d2 = Department.objects.create(name='Art')
            d3 = Department.objects.create(name='Business')

            #INITIALIZE MAJOR, MINOR TABLES
            Major.objects.create(name='BS in Computer Science', subject=d1)
            Major.objects.create(name='BA in Computer Science', subject=d1)
            Major.objects.create(name='Fine Arts', subject=d2)
            Major.objects.create(name='Art Education', subject=d2)
            Major.objects.create(name='Finance', subject=d3)
            Major.objects.create(name='Accounting', subject=d3)
            Major.objects.create(name='Mathematics', subject=d)
            Major.objects.create(name='Actuarial Science', subject=d)

            Minor.objects.create(name='Mathematics', subject=d)
            Minor.objects.create(name='Statistics', subject=d)
            Minor.objects.create(name='Applied Mathematics', subject=d)
            Minor.objects.create(name='Computer Science', subject=d1)
            Minor.objects.create(name='Cybersecurity', subject=d1)
            Minor.objects.create(name='Finance', subject=d3)

            #CREATE NEW HighImpactExperience ENTRY
            hie = HighImpactExperience.objects.create(name='Immersive and Service Learning Courses', RTX_name='Immersive Learning')
            hie.Freshman_desc = 'Watch reflections of Xavier students who have participated in immersive and service learning academic experiences.Use an Advanced Search in Self Service to explore Immersive and Service Learning Attributed Courses during registration.'
            hie.Sophomore_desc = 'Use an Advanced Search in Self Service to explore Immersive and Service Learning Attributed Courses during registration. ILE and SERL courses are available in the Core, as electives, and within many majors'
            hie.Junior_desc = 'Use an Advanced Search in Self Service to explore Immersive and Service Learning Attributed Courses during registration. ILE and SERL courses are available in the Core, as electives, and within many majors'
            hie.Senior_desc = 'Many ILE and SERL Attributed Courses are integrated into Capstone and Community Engaged Research experiences in your major. Ask your advisor, or use an Advanced Search to explore these integrated experiences.'
            hie.save()

            #-create Professor
            u = User.objects.create_user(username='mikeyg', last_name='Goldweber', email='goldweber@xavier.edu', first_name='Michael', password="mikey_scotch")
            u.groups.add(prof_group)
            p = Profile.objects.create(user=u, prefix='Dr.', role=Profile.PROFESSOR)
            dept=Department.objects.get(name="Computer Science")
            Professor.objects.create(prof=p, department=dept, degree_desc="PhD in Computer Science, University of Michigan 1969")

            #-create AdminAssistant
            u = User.objects.create_user(username='donnaw', last_name='Wallace', email='wallace@xavier.edu', first_name='Donna', password="donna_pw")
            u.groups.add(aa_group)
            p = Profile.objects.create(user=u, role=Profile.ADMINASSISTANT)
            dept=Department.objects.get(name="Computer Science")
            AdminAssistant.objects.create(prof=p, department=dept)

            #-create Students
            u = User.objects.create_user(username='kolleng', last_name='Gruizenga', email='gruizengak@xavier.edu', first_name='Kollen', password='test_kg_pw')
            u.groups.add(stud_group)
            p = Profile.objects.create(user=u, suffix='II', role=Profile.STUDENT)
            s = Student.objects.create(prof=p, schoolyear=Student.SENIOR)
            majors=[Major.objects.get(name="BS in Computer Science"), Major.objects.get(name="Finance")]
            minors=[Minor.objects.get(name="Mathematics")]
            for m in majors:
                s.major.add(m)
            for m in minors:
                s.minor.add(m)
            s.save()

            u = User.objects.create_user(username='aaronr', last_name='Ripley', email='ripleya@xavier.edu', first_name='Aaron', password='test_ar_pw')
            u.groups.add(stud_group)
            p = Profile.objects.create(user=u, prefix='Mr.', role=Profile.STUDENT)
            s = Student.objects.create(prof=p, schoolyear=Student.JUNIOR)
            majors=[Major.objects.get(name="BS in Computer Science")]
            for m in majors:
                s.major.add(m)
            s.save()
            
        except:
            raise CommandError('DB-initialization failed.')





# #--OLD
# user = User.objects.create_user('test', 'test@google.com', 'testpassword')
#             #Profiles.objects.create(user, '')
#             user.user_permissions.check()
#             user.user_permissions.add(perm obj)
#             user.get_all_permissions()
#             user.user_permissions.clear()