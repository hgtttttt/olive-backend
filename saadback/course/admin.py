from django.contrib import admin

# Register your models here.
from course.models import Subject, Course, CourseTime, CourseUser, CourseSubject

admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(CourseTime)
admin.site.register(CourseUser)
admin.site.register(CourseSubject)
