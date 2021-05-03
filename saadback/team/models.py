from django.contrib.auth.models import User
from django.db import models

normal_length = 100
long_length = 400

# Create your models here.

class Team(models.Model):
	class Meta:
		db_table = "team"
	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='team')
	name = models.CharField(max_length=normal_length)
	description = models.CharField(max_length=long_length, blank=True)
	qrcode = models.TextField(blank=True)
	baccount = models.CharField(max_length=normal_length, blank=True)
	tel = models.CharField(max_length=normal_length, blank=True)
	mail = models.CharField(max_length=normal_length, blank=True)
	website = models.CharField(max_length=normal_length, blank=True)
	logo = models.TextField(blank=True)
	teacher = models.CharField(max_length=normal_length, blank=True)
	student_num = models.IntegerField(default=0)
	addTime = models.DateTimeField(auto_now_add=True)

