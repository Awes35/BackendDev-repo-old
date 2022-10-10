from rest_framework import serializers

from .models import (
    HighImpactExperiences,
    Departments,
    Faculty,
    Courses,
    Majors,
    Minors,
    Students
)

class HighImpactExperiencesSerializer(serializers.ModelSerializer):

    class Meta:
        model = HighImpactExperiences
        fields = [
            "name",
            "RTX_name",
            "Freshman_desc",
            "Sophomore_desc",
            "Junior_desc",
            "Senior_desc",
            "creation_date"
        ]

class DepartmentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Departments
        fields = [
            "name"
        ]

class FacultySerializer(serializers.ModelSerializer):

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

class CoursesSerializer(serializers.ModelSerializer):

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

class MajorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Majors
        fields = [
            "name",
            "subject"
        ]

class MinorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Minors
        fields = [
            "name",
            "subject"
        ]

class StudentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Students
        fields = [
            "student_id",
            "first_name",
            "last_name",
            "major",
            "minor"
        ]