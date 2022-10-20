from django.db import models

# Create models here. A model is basically a database layout with additional metadata
#MUST STAGE MIGRATION: python manage.py makemigrations data
# > will then have to create/synch databases as defined in BackendDev/settings.py

class HighImpactExperiences(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    RTX_name = models.CharField(max_length=50)
    Freshman_desc = models.CharField(max_length=200)
    Sophomore_desc = models.CharField(max_length=200)
    Junior_desc = models.CharField(max_length=200)
    Senior_desc = models.CharField(max_length=200)
    creation_date = models.DateTimeField('date created')


class Departments(models.Model):
    name = models.CharField(max_length=50)


class Faculty(models.Model):
    faculty_id = models.IntegerField(default=000000000, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    prefix = models.CharField(max_length=4)
    suffix = models.CharField(max_length=4)
    department = models.ForeignKey(Departments, null=True, on_delete=models.SET_NULL)


class Courses(models.Model):
    crn = models.IntegerField(default=00000, primary_key=True)
    title = models.CharField(max_length=50)
    desc_text = models.CharField(max_length=200)
    course_num = models.IntegerField(default=000)
    subject = models.ForeignKey(Departments, null=True, on_delete=models.SET_NULL)
    instructor = models.ForeignKey(Faculty, null=True, on_delete=models.SET_NULL)
    credit_hours = models.IntegerField()


class Majors(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Departments, null=True, on_delete=models.SET_NULL)


class Minors(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Departments, null=True, on_delete=models.SET_NULL)


class Students(models.Model):
    student_id = models.IntegerField(default=000000000, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    major = models.ForeignKey(Majors, null=True, on_delete=models.SET_NULL)
    minor = models.ForeignKey(Minors, null=True, on_delete=models.SET_NULL)

class CalendarEvent(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    organizer = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    startTime = models.CharField(max_length=100)
    endTime = models.CharField(max_length=100)