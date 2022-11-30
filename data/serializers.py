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
            "id",
            "name",
        ]
        extra_kwargs = {"id": {'read_only':True}}



class MajorSerializer(serializers.ModelSerializer):
    subject = serializers.SlugRelatedField(slug_field='name', queryset=Department.objects.all())

    class Meta:
        model = Major
        fields = [
            "id",
            "name",
            "subject"
        ]
        extra_kwargs = {"id": {'read_only':True}}



class MinorSerializer(serializers.ModelSerializer):
    subject = serializers.SlugRelatedField(slug_field='name', queryset=Department.objects.all())

    class Meta:
        model = Minor
        fields = [
            "id",
            "name",
            "subject"
        ]
        extra_kwargs = {"id": {'read_only':True}}



class HighImpactExperienceSerializer(serializers.ModelSerializer):
    area = serializers.SlugRelatedField(slug_field='id', queryset=Department.objects.all())
    advisor = serializers.SlugRelatedField(slug_field='id', queryset=Professor.objects.all()) #? wip

    class Meta:
        model = HighImpactExperience
        fields = [
            "id",
            "name",
            "RTX_name",
            "area",
            "advisor",
            "Freshman_desc",
            "Sophomore_desc",
            "Junior_desc",
            "Senior_desc",
            "creation_date"
        ]
        extra_kwargs = {"creation_date": {'read_only':True}, "id": {'read_only':True}}



class EventSerializer(serializers.ModelSerializer):
    hie = serializers.SlugRelatedField(slug_field='id', queryset=HighImpactExperience.objects.all())

    class Meta:
        model = Event
        fields = [
            "id", #-user specified
            "name",
            "start_time",
            "end_time",
            "creation_time",
            # "modified_time",
            "url",
            "location",
            "categories",
            "organizer",
            "description",
            "hie"
        ]
        extra_kwargs = {"creation_time": {'read_only': True}}



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            # "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password"
        ]
        extra_kwargs = {"password": {'write_only': True}}#, "id": {'read_only':True}}



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
        extra_kwargs = {"role": {'read_only':True}}



class StudentSerializer(serializers.ModelSerializer):
    prof = ProfileSerializer(many=False)
    major = serializers.SlugRelatedField(many=True, slug_field='id', queryset=Major.objects.all(), allow_null=True, default=None)
    minor = serializers.SlugRelatedField(many=True, slug_field='id', queryset=Minor.objects.all(), allow_null=True, default=None)

    class Meta:
        model = Student
        fields = [
            "id",
            "prof",
            "major",
            "minor",
            "schoolyear"
        ]
        extra_kwargs = {"id": {'read_only':True}}
    
    def create(self, validated_data):
        stud_group, created = Group.objects.get_or_create(name="Student")
        print(f"CREATE DATA\n{validated_data}")
        prof_data = validated_data.pop("prof")
        user_data = prof_data.pop("user")

        majors = validated_data.pop("major")
        minors = validated_data.pop("minor")

        pw = user_data.pop("password") #--handle password separately (need to encrypt)
        pw = make_password(pw)

        u = User.objects.create(password=pw, **user_data)
        u.groups.add(stud_group) #--add user to Student perms group
        p = Profile.objects.create(user=u, role=Profile.STUDENT, **prof_data)
        s = Student.objects.create(prof=p, **validated_data)

        if majors is not None:
            for m in majors:
                s.major.add(m)
        if minors is not None:
            for m in minors:
                s.minor.add(m)
        s.save()

        return s
    
    def update(self, instance, validated_data):
        print(f"UPDATE DATA\n{validated_data}")
        prof_data = {}
        user_data = {}
        if "prof" in validated_data.keys():
            prof_data = validated_data.pop("prof")
        if "user" in prof_data.keys():
            user_data = prof_data.pop("user")
        
        profile = instance.prof
        user = profile.user 

        profile.prefix = prof_data.get("prefix", profile.prefix)
        profile.suffix = prof_data.get("suffix", profile.suffix)
        profile.role = prof_data.get("role", profile.role)
        profile.save()

        user.username = user_data.get("username", user.username)
        user.email = user_data.get("email", user.email)
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        if "password" in user_data.keys():
            user.password = make_password(user_data.get("password"))
        user.save()
        
        # return instance
        return super().update(instance, validated_data)



class ProfessorSerializer(serializers.ModelSerializer):
    prof = ProfileSerializer(many=False)
    department = serializers.SlugRelatedField(slug_field='id', queryset=Department.objects.all())

    class Meta:
        model = Professor
        fields = [
            "id",
            "prof",
            "department",
            "degree_desc"
        ]
        extra_kwargs = {"id": {'read_only':True}}
    
    def create(self, validated_data):
        prof_group, created = Group.objects.get_or_create(name="Professor")
        print(f"\n{validated_data}")
        prof_data = validated_data.pop("prof")
        user_data = prof_data.pop("user")

        pw = user_data.pop("password") #--handle password separately (need to encrypt)
        pw = make_password(pw)

        u = User.objects.create(password=pw, **user_data)
        u.groups.add(prof_group) #--add user to Professor perms group
        p = Profile.objects.create(user=u, role=Profile.PROFESSOR, **prof_data)
        s = Professor.objects.create(prof=p, **validated_data)
        return s
    
    def update(self, instance, validated_data):
        print(f"UPDATE DATA\n{validated_data}")
        prof_data = {}
        user_data = {}
        if "prof" in validated_data.keys():
            prof_data = validated_data.pop("prof")
        if "user" in prof_data.keys():
            user_data = prof_data.pop("user")
        
        profile = instance.prof
        user = profile.user 

        profile.prefix = prof_data.get("prefix", profile.prefix)
        profile.suffix = prof_data.get("suffix", profile.suffix)
        profile.role = prof_data.get("role", profile.role)
        profile.save()

        user.username = user_data.get("username", user.username)
        user.email = user_data.get("email", user.email)
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        if "password" in user_data.keys():
            user.password = make_password(user_data.get("password"))
        user.save()
        
        # return instance
        return super().update(instance, validated_data)



class AdminAssistantSerializer(serializers.ModelSerializer):
    prof = ProfileSerializer(many=False)
    department = serializers.SlugRelatedField(slug_field='id', queryset=Department.objects.all())

    class Meta:
        model = AdminAssistant
        fields = [
            "id",
            "prof",
            "department"
        ]
        extra_kwargs = {"id": {'read_only':True}}
    
    def create(self, validated_data):
        aa_group, created = Group.objects.get_or_create(name="AdminAssistant")
        print(f"\n{validated_data}")
        prof_data = validated_data.pop("prof")
        user_data = prof_data.pop("user")

        pw = user_data.pop("password") #--handle password separately (need to encrypt)
        pw = make_password(pw)

        u = User.objects.create(password=pw, **user_data)
        u.groups.add(aa_group) #--add user to AdminAssistant perms group
        p = Profile.objects.create(user=u,role=Profile.ADMINASSISTANT, **prof_data)
        s = AdminAssistant.objects.create(prof=p, **validated_data)
        return s
    
    def update(self, instance, validated_data):
        print(f"UPDATE DATA\n{validated_data}")
        prof_data = {}
        user_data = {}
        if "prof" in validated_data.keys():
            prof_data = validated_data.pop("prof")
        if "user" in prof_data.keys():
            user_data = prof_data.pop("user")
        
        profile = instance.prof
        user = profile.user 

        profile.prefix = prof_data.get("prefix", profile.prefix)
        profile.suffix = prof_data.get("suffix", profile.suffix)
        profile.role = prof_data.get("role", profile.role)
        profile.save()

        user.username = user_data.get("username", user.username)
        user.email = user_data.get("email", user.email)
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        if "password" in user_data.keys():
            user.password = make_password(user_data.get("password"))
        user.save()
        
        # return instance
        return super().update(instance, validated_data)



class CourseSerializer(serializers.ModelSerializer):
    subject = serializers.SlugRelatedField(slug_field='id', queryset=Department.objects.all())
    instructor = serializers.SlugRelatedField(slug_field='id', queryset=Professor.objects.all()) #?? WIP
    
    class Meta:
        model = Course
        fields = [
            "crn",
            "title",
            "course_num",
            "subject",
            "instructor",
            "credit_hours",
            "desc_text"
        ]

