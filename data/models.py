from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
# from django.conf import settings.AUTH_USER_MODEL

# Create models here. A model is basically a database layout with additional metadata
#MUST STAGE MIGRATION: python manage.py makemigrations data
# > will then have to create/synch databases as defined in BackendDev/settings.py


#with perms groups: Professors, Students, Admins
class Profile(models.Model):
    STUDENT = 'ST'
    PROFESSOR = 'PR'
    ADMINASSISTANT = 'AA'
    ROLES_CHOICES = [
        (STUDENT, 'Student'),
        (PROFESSOR, 'Professor'),
        (ADMINASSISTANT, 'AdminAssistant')
    ]
    user = models.OneToOneField(
        User,
        null=False, #DB cant store field as NULL
        blank=False, #field not allowed to be blank
        on_delete=models.CASCADE,
        related_name='users' #ProfileObj.users.all() - returns all User obj rel. to Profile
    )
    prefix = models.CharField(max_length=4, blank=True) #field can be blank
    suffix = models.CharField(max_length=4, blank=True) #field can be blank
    role = models.CharField(
        max_length=2,
        choices=ROLES_CHOICES,
        null=False, #DB cant store field as NULL
        blank=False, #field not allowed to be blank
        #default=STUDENT
    )


class Department(models.Model): #Superuser will create
    name = models.CharField(max_length=50, null=False, blank=False) #DB cant store field as NULL, field can't be blank


class Major(models.Model): #AdminAssistant will create
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(
        Department, 
        null=False, #DB cant store field as NULL
        blank=False, #field not allowed to be blank
        on_delete=models.PROTECT, #can't delete a Department that has Majors assigned to it
        related_name='major_depts' #maj.major_depts.all() - all Departments obj rel. to Major
    )


class Minor(models.Model): #AdminAssistant will create
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(
        Department, 
        null=False, #DB cant store field as NULL
        blank=False, #field not allowed to be blank
        on_delete=models.PROTECT, #can't delete a Department that has Minors assigned to it
        related_name='minor_depts' #min.minor_depts.all() - all Departments obj rel. to Minor
    )


class Student(models.Model): #Any can create
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    GRADUATE = 'GR'
    YEAR_CHOICES = [
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
        (GRADUATE, 'Graduate')
    ]
    # stud_id = models.PositiveIntegerField(primary_key=True, validators=[MaxValueValidator(999999999)])
    prof = models.ForeignKey(
        Profile, 
        null=False, #DB cant store field as NULL
        blank=False, #field not allowed to be blank
        on_delete=models.CASCADE,
        related_name='stud_profiles' #s1.stud_profiles.all() - all Profile obj rel. to Student
    )
    major = models.ManyToManyField(
        Major, 
        blank=True, #field is allowed to be blank
        default=None,
        related_name='stud_majors' #s1.stud_majors.all() - all Major obj rel. to Student
    )
    minor = models.ManyToManyField(
        Minor, 
        blank=True, #field is allowed to be blank
        default=None,
        related_name='stud_minors' #s1.stud_minors.all() - all Minor obj rel. to Student
    )
    schoolyear = models.CharField(
        max_length=2,
        choices=YEAR_CHOICES,
        null=False, #DB cant store field as NULL
        blank=False #field not allowed to be blank
        # default=FRESHMAN
    )


class Professor(models.Model): #AdminAssistant will create
    prof = models.ForeignKey(
        Profile, 
        null=False, #DB cant store field as NULL
        blank=False, #field not allowed to be blank
        on_delete=models.CASCADE,
        related_name='prof_profiles' #p1.prof_profiles.all() - all Profile obj rel. to Professor
    )
    department = models.ForeignKey(
        Department, 
        null=False, #DB cant store field as NULL
        blank=False, #field not allowed to be blank
        on_delete=models.PROTECT, #can't delete a Department that has Professors assigned to it
        related_name='prof_depts' #p1.prof_depts.all() - all Department obj rel. to Professor
    )
    degree_desc = models.CharField(max_length=300)


class AdminAssistant(models.Model): #Superuser/other AdminAssistant's will create
    prof = models.ForeignKey(
        Profile,
        null=False, #DB cant store field as NULL
        blank=False, #field not allowed to be blank
        on_delete=models.CASCADE,
        related_name='aa_profiles'  #aa1.aa_profiles.all() - all Profile obj rel. to AdminAssistant
    )
    department = models.ForeignKey(
        Department,
        null=True, #DB can store empty field as NULL
        blank=True, #field allowed to be blank -- entered 
        on_delete=models.PROTECT, #can't delete a Department that has AdminAssistants assigned to it
        related_name='aa_depts'  #aa1.aa_depts.all() - all Department obj rel. to AdminAssistant
    )


class Course(models.Model): #AdminAssistant or Professor will create
    crn = models.PositiveIntegerField(primary_key=True, null=False, blank=False, validators=[MaxValueValidator(99999)]) #-- when update, doesn't delete old entry
    title = models.CharField(max_length=50, null=False, blank=False)
    desc_text = models.CharField(max_length=200, null=False, blank=True)
    course_num = models.IntegerField(default=000, null=False, blank=False)
    subject = models.ForeignKey(
        Department, 
        null=False, #DB cant store field as NULL
        blank=False, #field not allowed to be blank
        on_delete=models.PROTECT, #can't delete a Department that has Courses assigned to it
        related_name='crs_depts' #c1.crs_depts.all() - all Departments obj rel. to Course
    )
    instructor = models.ForeignKey(
        Professor, 
        null=True, #DB can store empty field as NULL
        blank=True, #field allowed to be blank
        on_delete=models.SET_NULL, #course could be without an instructor
        related_name='crs_profs' #c1.crs_profs.all() - all Professor obj rel. to Course
    ) 
    credit_hours = models.IntegerField(null=False, blank=False)


class HighImpactExperience(models.Model): #AdminAssistant or Professor will create
    name = models.CharField(max_length=50)
    RTX_name = models.CharField(max_length=50)
    Freshman_desc = models.CharField(max_length=200)
    Sophomore_desc = models.CharField(max_length=200)
    Junior_desc = models.CharField(max_length=200)
    Senior_desc = models.CharField(max_length=200)
    creation_date = models.DateTimeField('date created', auto_now_add=True)

    area = models.ForeignKey(
        Department,
        null=True, #DB can store empty field as NULL
        blank=True, #field allowed to be blank
        on_delete=models.SET_NULL,
        related_name='hie_depts' #h1.hie_depts.all() - all Department obj rel. to HighImpactExperience
    )
    advisor = models.ForeignKey(
        Professor,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='hie_professor'
    )


class Event(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, validators=[MaxValueValidator(9999999)]) #-- when update, doesn't delete old entry
    name = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    creation_time = models.DateTimeField('date created', auto_now_add=True)
    # modified_time = models.DateTimeField()
    url = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    categories = models.CharField(max_length=100) # event_type and event_tags ??
    organizer = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    hie = models.ForeignKey(
        HighImpactExperience,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='event_hie'
    )

