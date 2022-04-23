from django.db import models
from django.contrib.auth.models import User as djUser
from django.contrib.sessions.models import Session
from datetime import date


class AuthUser(djUser):
    class Meta:
        proxy = True


class University(models.Model):
    code = models.CharField(max_length=8, default=None, primary_key=True)
    name = models.CharField(max_length=128, default=None)

    def __str__(self):
        return f"{self.name}"


class College(models.Model):
    code = models.CharField(max_length=8, default=None, primary_key=True)
    name = models.CharField(max_length=128, default=None)
    university = models.ForeignKey(
        University, on_delete=models.CASCADE, to_field="code")

    def __str__(self):
        return f"{self.name}"


class Department(models.Model):
    code = models.CharField(max_length=8, default=None, primary_key=True)
    name = models.CharField(max_length=128, default=None)
    college = models.ForeignKey(
        College, on_delete=models.CASCADE, to_field="code")

    def __str__(self):
        return f"{self.name} ({self.college.name} of {self.college.university.name})"


class User(AuthUser):
    gender = models.CharField(max_length=8,default=None, null=True)
    birth_date = models.DateField(default=date.today)
    email_status = models.BooleanField(default=False)
    registration = models.IntegerField(unique=True, default=None, null=True)
    university = models.ForeignKey(
        University, on_delete=models.CASCADE, to_field="code")
    college = models.ForeignKey(
        College, on_delete=models.CASCADE, to_field="code", null=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, to_field="code", null=True)

    class Meta:
        abstract = True


class Student(User):
    semester = models.IntegerField(default=1)

    def __str__(self):
        return f"Name: {self.first_name} {self.last_name}"


class Tutor(User):
    registraion = None
    position = models.CharField(max_length=128, default="Teaching Assistant")

    def __str__(self):
        return f"Name: {self.first_name} {self.last_name}"


class Subject(models.Model):
    tutors = models.ManyToManyField(Tutor)
    description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=64, default=None)
    students = models.ManyToManyField(Student, null=True, blank=True)
    code = models.CharField(
        max_length=32, primary_key=True, unique=True, default=None)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, to_field='code', null=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Answer(models.Model):
    answer = models.TextField()
    tutor = models.ForeignKey(
        Tutor, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"A: {self.answer}"


class Question(models.Model):
    student = models.ManyToManyField(Student)
    question = models.TextField(null=True)
    answer = models.OneToOneField(
        Answer, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, to_field="code", null=True)

    def __str__(self):
        return f"Q: {self.question}"


class Announcement(models.Model):
    text = models.TextField(null=True)
    urgency = models.CharField(max_length=32, default="Neutral")
    tutor = models.ForeignKey(
        Tutor, on_delete=models.CASCADE)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, to_field="code", null=True)

    def __str__(self):
        return f"Announcement: {self.text} by ({self.tutor.name})"


class Topic(models.Model):
    number = models.IntegerField()
    date = models.DateField(default=date.today)
    text = models.TextField(null=True, blank=True)
    label = models.CharField(max_length=8, default="External")
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE,  to_field="code")

    def __str__(self):
        return f"({self.number}) {self.label}"


class Resource(models.Model):
    link = models.CharField(max_length=512)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.link}"


data_models = {'subject': Subject, 'student': Student, 'tutor': Tutor,
           'question': Question, 'announcement': Announcement, 'resource': Resource,
           'college': College, 'department': Department, 'topic': Topic,
           'university': University, 'answer': Answer}
