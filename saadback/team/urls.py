from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('getteamdetail', views.get_team_info, name='get_team_info'),

    path('changeteamdetail', views.change_detail, name='change_detail'),

    path('register', views.register, name='register'),
]