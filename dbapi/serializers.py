from rest_framework import serializers
from .models import data_models


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = data_models['question']
        fields = [field.name for field in model._meta.fields]


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = data_models['announcement']
        fields = [field.name for field in model._meta.fields]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = data_models['student']
        fields = [field.name for field in model._meta.fields]
        fields.remove('user_ptr')
        fields.remove('password')


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = data_models['tutor']
        fields = [field.name for field in model._meta.fields]
        fields.remove('user_ptr')
        fields.remove('password')


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = data_models['topic']
        fields = [field.name for field in model._meta.fields]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = data_models['subject']
        fields = [field.name for field in model._meta.fields]


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = data_models['college']
        fields = [field.name for field in model._meta.fields]


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = data_models['university']
        fields = [field.name for field in model._meta.fields]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = data_models['department']
        fields = [field.name for field in model._meta.fields]


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = data_models['resource']
        fields = [field.name for field in model._meta.fields]

model_serializers = {'subject': SubjectSerializer, 'student': StudentSerializer, 'tutor': TutorSerializer,
           'question': QuestionSerializer, 'announcement': AnnouncementSerializer, 'resource': ResourceSerializer,
           'college': CollegeSerializer, 'department': DepartmentSerializer, 'topic': TopicSerializer, 'university': UniversitySerializer}