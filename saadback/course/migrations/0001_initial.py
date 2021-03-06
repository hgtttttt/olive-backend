# Generated by Django 2.2 on 2021-01-31 11:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('team', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=400)),
                ('picture', models.TextField(blank=True)),
                ('teacher', models.CharField(blank=True, max_length=100)),
                ('addtime', models.DateTimeField(auto_now_add=True)),
                ('expirytime', models.DateTimeField()),
                ('link', models.CharField(blank=True, max_length=100)),
                ('student_num', models.IntegerField(default=0)),
                ('tid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='team.Team')),
            ],
            options={
                'db_table': 'course',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'subject',
            },
        ),
        migrations.CreateModel(
            name='CourseUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('addtime', models.DateTimeField(auto_now_add=True)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='course.Course')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'course_student',
            },
        ),
        migrations.CreateModel(
            name='CourseTime',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('starttime', models.DateTimeField(auto_now_add=True)),
                ('endtime', models.DateTimeField(auto_now_add=True)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_time', to='course.Course')),
            ],
            options={
                'db_table': 'course_time',
            },
        ),
        migrations.CreateModel(
            name='CourseSubject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_subject', to='course.Course')),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_subject', to='course.Subject')),
            ],
            options={
                'db_table': 'course_subject',
            },
        ),
    ]
