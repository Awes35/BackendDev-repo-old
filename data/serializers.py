# from multiprocessing import Event
from rest_framework import serializers
from django.contrib.auth.models import User, Group #, Permission
from django.contrib.auth.hashers import make_password

from .models import (
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



class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = [
            "name",
            "id"
        ]
        extra_kwargs = {"id": {'read_only':True}}


class MajorSerializer(serializers.ModelSerializer):
    subject = serializers.SlugRelatedField(slug_field='name', queryset=Department.objects.all())

    class Meta:
        model = Major
        fields = [
            "name",
            "subject"
        ]


class MinorSerializer(serializers.ModelSerializer):
    subject = serializers.SlugRelatedField(slug_field='name', queryset=Department.objects.all())

    class Meta:
        model = Minor
        fields = [
            "name",
            "subject"
        ]


class HighImpactExperienceSerializer(serializers.ModelSerializer):
    area = serializers.SlugRelatedField(slug_field='name', queryset=Department.objects.all())

    class Meta:
        model = HighImpactExperience
        fields = [
            "name",
            "RTX_name",
            "Freshman_desc",
            "Sophomore_desc",
            "Junior_desc",
            "Senior_desc",
            "creation_date",
            "area",
            "advisor"
        ]


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = [
            "__all__"
        ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password"
        ]
        extra_kwargs = {"id": {'read_only':True}, "password": {'write_only': True}}



class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Profile
        fields = [
            "user",
            "prefix",
            "suffix",
            "role"
        ]


class StudentSerializer(serializers.ModelSerializer):
    prof = ProfileSerializer(many=False)
    major = serializers.SlugRelatedField(slug_field='name', queryset=Major.objects.all(), allow_null=True, default=None)
    minor = serializers.SlugRelatedField(slug_field='name', queryset=Minor.objects.all(), allow_null=True, default=None)

    class Meta:
        model = Student
        fields = [
            "id",
            "prof",
            "major",
            "minor",
            "schoolyear"
        ]
        extra_kwargs = {"id": {'read_only':True}}#, "minor": {'allow_null':True}}
    
    def create(self, validated_data):
        stud_group, created = Group.objects.get_or_create(name="Student")
        print(f"\n{validated_data}")
        prof_data = validated_data.pop("prof")
        user_data = prof_data.pop("user")

        pw = user_data.pop("password") #--handle password separately (need to encrypt)
        pw = make_password(pw)

        u = User.objects.create(password=pw, **user_data)
        u.groups.add(stud_group) #--add user to Student perms group
        p = Profile.objects.create(user=u, **prof_data)
        s = Student.objects.create(prof=p, **validated_data)
        return s
    
    def update(self, instance, validated_data):
        print(f"\n{validated_data}")
        prof_data = validated_data.pop("prof")
        user_data = prof_data.pop("user")

        profile = instance.prof
        user = profile.user #assuming you specify nested attributes (not hyperlink)

        # instance.major = Major.objects.get(name=validated_data.get("major", instance.major))
        # instance.minor = Minor.objects.get(name=validated_data.get("minor", instance.minor))

        instance.major = validated_data.get('major', instance.major)
        instance.minor = validated_data.get('minor', instance.minor)
        instance.schoolyear = validated_data.get("schoolyear", instance.schoolyear)
        instance.save()

        profile.prefix = prof_data.get("prefix", profile.prefix)
        profile.suffix = prof_data.get("suffix", profile.suffix)
        profile.role = prof_data.get("role", profile.role)
        profile.save()

        user.username = user_data.get("username", user.username)
        user.email = user_data.get("email", user.email)
        user.first_name = user_data.get("first_name", user.last_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.password = user_data.get("password", user.password)
        user.save()
        
        return instance




class ProfessorSerializer(serializers.ModelSerializer):
    prof = ProfileSerializer(many=False)
    department = serializers.SlugRelatedField(slug_field='name', queryset=Department.objects.all())

    class Meta:
        model = Professor
        fields = [
            "prof",
            "department",
            "degree_desc"
        ]
    
    # prof_group, created = Group.objects.get_or_create(name="Professor")


class AdminAssistantSerializer(serializers.ModelSerializer):
    prof = ProfileSerializer(many=False)
    department = serializers.SlugRelatedField(slug_field='name', queryset=Department.objects.all())

    class Meta:
        model = AdminAssistant
        fields = [
            "prof",
            "department"
        ]

    # aa_group, created = Group.objects.get_or_create(name="AdminAssistant")

class CourseSerializer(serializers.ModelSerializer):
    subject = serializers.SlugRelatedField(slug_field='name', queryset=Department.objects.all())
    instructor = serializers.SlugRelatedField(slug_field='name', queryset=Professor.objects.all())
    
    class Meta:
        model = Course
        fields = [
            "crn",
            "title",
            "desc_text",
            "course_num",
            "subject",
            "instructor",
            "credit_hours"
        ]
