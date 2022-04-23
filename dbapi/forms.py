from .models import data_models
from django.forms import ModelForm, PasswordInput

class QuestionForm(ModelForm):
    class Meta:
        model = data_models['question']
        fields = [ field.name for field in model._meta.fields ]
class AnnouncementForm(ModelForm):
    class Meta:
        model = data_models['announcement']
        fields = [ field.name for field in model._meta.fields ]
class StudentForm(ModelForm):
    class Meta:
        model = data_models['student']
        fields = [ field.name for field in model._meta.fields ]
        widgets = {
            "passowrd": PasswordInput()
        }
class TutorForm(ModelForm):
    class Meta:
        model = data_models['tutor']
        fields = [ field.name for field in model._meta.fields ]
        widgets = {
            "passowrd": PasswordInput()
        }
class TopicForm(ModelForm):
    class Meta:
        model = data_models['topic']
        fields = [ field.name for field in model._meta.fields ]
class SubjectForm(ModelForm):
    class Meta:
        model = data_models['subject']
        fields = [ field.name for field in model._meta.fields ]
class CollegeForm(ModelForm):
    class Meta:
        model = data_models['college']
        fields = [ field.name for field in model._meta.fields ]
class UniversityForm(ModelForm):
    class Meta:
        model = data_models['university']
        fields = [ field.name for field in model._meta.fields ]
class DepartmentForm(ModelForm):
    class Meta:
        model = data_models['department']
        fields = [ field.name for field in model._meta.fields ]
class ResourceForm(ModelForm):
    class Meta:
        model = data_models['resource']
        fields = [ field.name for field in model._meta.fields ]

data_forms = {'subject': SubjectForm, 'student': StudentForm, 'tutor': TutorForm,
           'question': QuestionForm, 'announcement': AnnouncementForm, 'resource': ResourceForm,
           'college': CollegeForm, 'department': DepartmentForm, 'topic': TopicForm, 'university': UniversityForm}