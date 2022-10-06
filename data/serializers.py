
from rest_framework import serializers

from .models import (
    HighImpactExperiences,
    Departments,
    Faculty,
    Courses,
    Majors,
    Minors,
    Student
)

class SerializerHighImpactExperiences(serializers.ModelSerializer):

    class Meta:
        model = HighImpactExperiences
        fields = [
            "name",
            "RTX_Name",
            "Freshman_desc",
            "Sophomore_desc",
            "Junior_desc",
            "Senior_desc",
            "creation_date"
        ]

class SerializerDepartments(serializers.ModelSerializer):

    class Meta:
        model = Departments
        fields = [
            "name"
        ]

class SerializerFaculty(serializers.ModelSerializer):

    class Meta:
        model = Faculty
        fields = [
            "faculty_id",
            "first_name",
            "last_name",
            "prefix",
            "suffix",
            "department"
        ]

class SerializerCourses(serializers.ModelSerializer):

    class Meta:
        model = Courses
        fields = [
            "crn",
            "title",
            "desc_text",
            "course_num",
            "subject",
            "instructor",
            "credit_hours"
        ]

class SerializerMajors(serializers.ModelSerializer):

    class Meta:
        model = Majors
        fields = [
            "name",
            "subject"
        ]

class SerializerMinors(serializers.ModelSerializer):

    class Meta:
        model = Minors
        fields = [
            "name",
            "subject"
        ]

class SerializerStudents(serializers.ModelSerializer):

    class Meta:
        model = Students
        fields = [
            "student_id",
            "first_name",
            "last_name",
            "major",
            "minor"
        ]