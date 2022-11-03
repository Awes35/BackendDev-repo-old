from this import d
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group, Permission

from django.contrib.auth.backends import ModelBackend 


#call command via: python manage.py db_startup

GROUPS = ['Students', 'Professors', 'Admins']
MODELS = ['']
PERMISSIONS = ['view']


class Command(BaseCommand):
    help = 'Initialize databases with authenticated users for access'

    def handle(self, *args, **kwargs):
        try:
            user = User.objects.create_user('test', 'test@google.com', 'testpassword')
            #Profiles.objects.create(user, '')
            user.user_permissions.check()
            user.user_permissions.add(perm obj)
            user.get_all_permissions()
            user.user_permissions.clear()
        except:
            raise CommandError('DB-initialization failed.')


from django.contrib.contenttypes.models import ContentType
from data.models import Student
content_type = ContentType.objects.get_for_model(Student)
post_perm = Permission.objects.filter(content_type=content_type)
print([perm.codename for perm in post_perm])
#['add_students', 'change_students', 'delete_students', 'view_students']

Student.objects.create()
#need to add 'create user' api endpoint view

from data.models import Department
Department.objects.create(name='Psychology')
Department.objects.create(name='Science')

from data.models import Profile
u = User.objects.get(username='gosborn')
d = Department.objects.get(name='Psychology')
Profile.objects.create(user=u, department=d)

#shell: python manage.py shell


# create a HIE entry (row)
from data.models import HighImpactExperience
HighImpactExperience.objects.create(name='Immersive and Service Learning Courses', RTX_name='Immersive Learning')
hie = HighImpactExperience.objects.get(name='Immersive and Service Learning Courses')
hie.Freshman_desc = 'Watch reflections of Xavier students who have participated in immersive and service learning academic experiences.Use an Advanced Search in Self Service to explore Immersive and Service Learning Attributed Courses during registration.'
hie.Sophomore_desc = 'Use an Advanced Search in Self Service to explore Immersive and Service Learning Attributed Courses during registration. ILE and SERL courses are available in the Core, as electives, and within many majors'
hie.Junior_desc = 'Use an Advanced Search in Self Service to explore Immersive and Service Learning Attributed Courses during registration. ILE and SERL courses are available in the Core, as electives, and within many majors'
hie.Senior_desc = 'Many ILE and SERL Attributed Courses are integrated into Capstone and Community Engaged Research experiences in your major. Ask your advisor, or use an Advanced Search to explore these integrated experiences.'
hie.save()




