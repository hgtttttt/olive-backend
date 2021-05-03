from django.contrib.auth.models import User
from django.db import models

from team.models import Team

normal_length = 100
long_length = 400

# Create your models here.

class Subject(models.Model):
	class Meta:
		db_table = "subject"
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=normal_length)


class Course(models.Model):
	class Meta:
		db_table = "course"
	id = models.AutoField(primary_key=True)
	tid = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="course")
	name = models.CharField(max_length=normal_length)
	description = models.CharField(max_length=long_length, blank=True)
	picture = models.TextField(blank=True)
	teacher = models.CharField(max_length=normal_length, blank=True)
	addTime = models.DateTimeField(auto_now_add=True)
	expiryTime = models.DateTimeField(auto_now_add=True)
	link = models.CharField(max_length=normal_length, blank=True)
	student_num = models.IntegerField(default=0)


class CourseSubject(models.Model):
	class Meta:
		db_table = "course_subject"
	id = models.AutoField(primary_key=True)
	cid = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_subject")
	sid = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="course_subject")


class CourseTime(models.Model):
	class Meta:
		db_table = "course_time"
		# ordering = ['-start_time']
	id = models.AutoField(primary_key=True)
	cid = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_time")
	startTime = models.DateTimeField()
	endTime = models.DateTimeField()


class CourseUser(models.Model):
	class Meta:
		db_table = "course_student"
	id = models.AutoField(primary_key=True)
	cid = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="student")
	uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course")
	addTime = models.DateTimeField(auto_now_add=True)
