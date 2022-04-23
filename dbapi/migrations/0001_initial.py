# Generated by Django 3.0.2 on 2020-03-30 21:38

import datetime
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('code', models.CharField(default=None, max_length=8, primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('code', models.CharField(default=None, max_length=8, primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=128)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbapi.College')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('description', models.TextField(blank=True, null=True)),
                ('name', models.CharField(default=None, max_length=64)),
                ('code', models.CharField(default=None, max_length=32, primary_key=True, serialize=False, unique=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dbapi.Department')),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('code', models.CharField(default=None, max_length=8, primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('gender', models.CharField(default=None, max_length=8, null=True)),
                ('birth_date', models.DateField(default=datetime.date.today)),
                ('email_status', models.BooleanField(default=False)),
                ('registration', models.IntegerField(default=None, null=True, unique=True)),
                ('semester', models.IntegerField(default=1)),
            ],
            options={
                'abstract': False,
            },
            bases=('dbapi.authuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('date', models.DateField(default=datetime.date.today)),
                ('text', models.TextField(blank=True, null=True)),
                ('label', models.CharField(default='External', max_length=8)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbapi.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=512)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbapi.Topic')),
            ],
        ),
        migrations.AddField(
            model_name='college',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbapi.University'),
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('gender', models.CharField(default=None, max_length=8, null=True)),
                ('birth_date', models.DateField(default=datetime.date.today)),
                ('email_status', models.BooleanField(default=False)),
                ('registration', models.IntegerField(default=None, null=True, unique=True)),
                ('position', models.CharField(default='Teaching Assistant', max_length=128)),
                ('college', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dbapi.College')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dbapi.Department')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbapi.University')),
            ],
            options={
                'abstract': False,
            },
            bases=('dbapi.authuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='topic',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbapi.Tutor'),
        ),
        migrations.AddField(
            model_name='subject',
            name='students',
            field=models.ManyToManyField(blank=True, null=True, to='dbapi.Student'),
        ),
        migrations.AddField(
            model_name='subject',
            name='tutors',
            field=models.ManyToManyField(to='dbapi.Tutor'),
        ),
        migrations.AddField(
            model_name='student',
            name='college',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dbapi.College'),
        ),
        migrations.AddField(
            model_name='student',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dbapi.Department'),
        ),
        migrations.AddField(
            model_name='student',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbapi.University'),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(null=True)),
                ('answer', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dbapi.Answer')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dbapi.Subject')),
                ('student', models.ManyToManyField(to='dbapi.Student')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='tutor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dbapi.Tutor'),
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(null=True)),
                ('urgency', models.CharField(default='Neutral', max_length=32)),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dbapi.Subject')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbapi.Tutor')),
            ],
        ),
    ]
