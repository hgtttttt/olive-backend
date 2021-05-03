from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('getlatest', views.get_last, name="get_last_course"),

    path('getpopular', views.get_popular, name="get_last_course"),

    path('getcoursedetail', views.get_detail, name="get_course_detail"),

    path('getcoursesbylabel', views.get_subject, name="get_course_subject"),

    path('changecourse', views.change_course, name="change_course"),

    # TODO: fix the time bug
    path('uploadcourse', views.upload_course, name="upload_course"),

    path('uploadcourse', views.upload_course, name="upload_course"),

    path('isjoined', views.is_joined, name="is_joined"),

    path('joincourse', views.join_course, name="join_course"),

    path('searchcourse', views.search_course, name="search_course"),

    path('delete', views.delete, name="delete"),
]