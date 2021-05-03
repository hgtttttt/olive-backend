import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from team.models import Team


def get_team_info(request):
    data = json.loads(request.body)
    id = data.get('id')
    print(id)
    if id is None:
        return JsonResponse({'error_code': 2, 'data': {}})
    team = Team.objects.filter(pk=id).first()
    if team is None:
        return JsonResponse({'error_code': 1, 'data': {}})
    else:
        result = {"id":team.id, "logo":team.logo, "qrcode":team.qrcode, "name":team.name, "teacher":team.teacher,
                  "description":team.description, "tel": team.tel, "mail": team.mail, "website": team.website}
        return JsonResponse({'error_code': 0, 'data': result})


def change_detail(request):
    data = json.loads(request.body)
    id = data.get('id')
    logo = data.get("logo")
    qrcode = data.get("qrcode")
    name = data.get("name")
    teacher = data.get("teacher")
    description = data.get("description")
    web = data.get("website")
    email = data.get("mail")
    tel = data.get("tel")
    print(id)
    if id is None:
        return JsonResponse({'error_code': 2, "msg": "error parameter"})
    team = Team.objects.filter(pk=id).first()
    if team is None:
        return JsonResponse({'error_code': 1, "msg": "team not exist"})
    else:
        team.logo = logo
        if qrcode != "":
            team.qrcode = qrcode
        team.name = name
        team.teacher = teacher
        team.description = description
        team.tel = tel
        team.website = web
        team.mail = email
        team.save()
        return JsonResponse({'error_code': 0})


#注册
def register(request):
    # data = json.loads(request.POST)
    data = json.loads(request.body)
    print(request.method)
    username = data.get("username")
    password = data.get("password")
    print(username)
    print(password)
    # name = request.POST.get("name")
    if username is None or password is None:
        return JsonResponse({'error_code': 2, 'data': {}})
    user = User.objects.filter(username=username).first()
    if user is not None:
        return JsonResponse({'error_code': 1, "msg": "name not unique"})
    user = User.objects.create_user(username=username, password=password)
    user.save()
    # login_user = authenticate(request, username=username, password=password)
    # if login_user:
    #     login(request, login_user)
        # print(1)
    team = Team.objects.create(user=user, name=username)
    team.save()
    return JsonResponse( {
        "error_code": 0,
        "data": {
          "id": team.pk,
          "username": user.username,
        }
      })
