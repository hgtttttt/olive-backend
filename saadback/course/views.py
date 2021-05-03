import datetime
import json

from django.utils import timezone
from fuzzywuzzy import fuzz
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
import course
from course.models import Course, CourseTime, CourseSubject, CourseUser
from course.tools import get_simple_info
from team.models import Team

last_courses={}
hot_courses={}


def find_last():
	global last_courses
	coursest = CourseTime.objects.filter(startTime__lte=datetime.datetime.now()).order_by('-startTime')
	result = []
	if coursest.count() < 4:
		for courset in coursest:
			# if courset.startTime<timezone.now():
			# 	break
			courset = courset.cid
			result.append(get_simple_info(courset))
			# result.append(json.dumps(courset.cid, default=lambda obj: obj.__dict__))
	else:
		i = 0
		for courset in coursest:
			# if courset.startTime<timezone.now():
			# 	break
			# courset = coursest[i].cid
			courset = courset.cid
			i+=1
			if i > 4:
				break
			result.append(get_simple_info(courset))
			# result.append(json.dumps(coursest[i].cid, default=lambda obj: obj.__dict__))
	# print(result)
	last_courses={'error_code': 0, 'data': result}
	print("find success")
	return True


def find_popular():
	global hot_courses
	courses = Course.objects.all().order_by('-student_num')
	result = []
	if courses.count() < 4:
		for course in courses:
			# courset = course
			result.append(get_simple_info(course))
			# result.append({"picture":courset.picture, "name":courset.name, "team":courset.tid.name, "description":courset.description})
			# result.append(json.dumps(course, default=lambda obj: obj.__dict__))
	else:
		i=0
		for course in courses:
			# courset = courses[i]
			i+=1
			if i > 4:
				break
			result.append(get_simple_info(course))
			# result.append(json.dumps(courses[i], default=lambda obj: obj.__dict__))
	hot_courses = {'error_code': 0, 'data': result}
	print("find success")
	return True


def debug():
	global hot_courses
	global last_courses
	print(last_courses)
	print(hot_courses)


def get_last(request):
	if request.method != "POST":
		return JsonResponse({'error_code': 1, 'msg': "not POST method"})
	global last_courses
	return JsonResponse(last_courses)
	# coursest = CourseTime.objects.filter(startTime__gte=datetime.datetime.now()).order_by('-startTime')
	# # print(coursest)
	# result = []
	# if coursest.count() < 4:
	# 	for courset in coursest:
	# 		# if courset.startTime<timezone.now():
	# 		# 	break
	# 		courset = courset.cid
	# 		result.append(get_simple_info(courset))
	# 		# result.append(json.dumps(courset.cid, default=lambda obj: obj.__dict__))
	# else:
	# 	i = 0
	# 	for courset in coursest:
	# 		# if courset.startTime<timezone.now():
	# 		# 	break
	# 		# courset = coursest[i].cid
	# 		courset = courset.cid
	# 		i+=1
	# 		if i > 4:
	# 			break
	# 		result.append(get_simple_info(courset))
	# 		# result.append(json.dumps(coursest[i].cid, default=lambda obj: obj.__dict__))
	# return JsonResponse({'error_code': 0, 'data': result})


def get_popular(request):
	if request.method != "POST":
		return JsonResponse({'error_code': 1, 'msg': "not POST method"})
	global hot_courses
	return JsonResponse(hot_courses)
	# courses = Course.objects.all().order_by('-student_num')
	# result = []
	# if courses.count() < 4:
	# 	for course in courses:
	# 		# courset = course
	# 		result.append(get_simple_info(course))
	# 		# result.append({"picture":courset.picture, "name":courset.name, "team":courset.tid.name, "description":courset.description})
	# 		# result.append(json.dumps(course, default=lambda obj: obj.__dict__))
	# else:
	# 	i=0
	# 	for course in courses:
	# 		# courset = courses[i]
	# 		i+=1
	# 		if i > 4:
	# 			break
	# 		result.append(get_simple_info(course))
	# 		# result.append(json.dumps(courses[i], default=lambda obj: obj.__dict__))
	# return JsonResponse({'error_code': 0, 'data': result})


def get_detail(request):
	if request.method != "POST":
		return JsonResponse({'error_code': 1, 'msg': "not POST method"})
	data = json.loads(request.body)
	course = Course.objects.filter(id=data.get("id")).first()
	if course is None:
		return JsonResponse({'error_code': 0, 'msg': "course not exist", })
	result = {"picture": course.picture, "name": course.name, "team": course.tid.name, "teamid": course.tid.id, "teacher": course.teacher,
	          "description": course.description, "link": course.link, "count": course.student_num,
	          "starttime": datetime.datetime.strftime(course.course_time.first().startTime, '%Y-%m-%d %H:%M:%S'),
	          "endtime": datetime.datetime.strftime(course.course_time.first().endTime, '%Y-%m-%d %H:%M:%S')}
	# result = json.dumps(course, default=lambda obj: obj.__dict__)
	# courses = Course.objects.all().order_by('student_num')
	# result = []
	# if courses.count()<4:
	# 	for course in courses:
	#
	# else:
	# 	for i in range(4):
	# 		result.append(json.dumps(courses[i], default=lambda obj: obj.__dict__))
	return JsonResponse({'error_code': 0, 'data': result})


def get_subject(request):
	if request.method != "POST":
		return JsonResponse({'error_code': 1, 'msg': "not POST method"})
	data = json.loads(request.body)
	coursess = CourseSubject.objects.filter(sid__id=data.get("label"))
	result = []
	for courses in coursess:
		courses = courses.cid
		result.append(get_simple_info(courses))
		# result.append(json.dumps(courses.cid, default=lambda obj: obj.__dict__))
	return JsonResponse({'error_code': 0, 'data': result})


def change_course(request):
	if request.method != "POST":
		return JsonResponse({'error_code': 1, 'msg': "not POST method"})
	data = json.loads(request.body)
	course = Course.objects.filter(pk=data.get("id")).first()
	if course is None:
		return JsonResponse({'error_code': 2, 'msg': "course not exist"})
	courseTime = course
	name = data.get('name')
	teacher = data.get('teacher')
	description = data.get('description')
	link = data.get('link')
	# TODO: change time
	startTime = data.get('startTime')
	endTime = data.get('endTime')
	image = data.get('image')
	course.name = name
	course.image = image
	startTime = datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
	endTime = datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
	# courseTime = CourseTime(addTime=addTime, endTime=endTime)
	# courseTime.save()
	courseTime = course.course_time.first()
	courseTime.startTime = startTime
	courseTime.endTime = endTime
	# course.course_time.create(startTime=startTime, endTime=endTime)
	if teacher != "":
		course.teacher = teacher
	if description != "":
		course.description = description
	if link != "":
		course.link = link
	course.save()
	courseTime.save()
	return JsonResponse({'error_code': 0})


def upload_course(request):
	if request.method != "POST":
		return JsonResponse({'error_code': 1, 'msg': "not POST method, it's "+request.method})
	data = json.loads(request.body)
	team = Team.objects.filter(pk=data.get("tid")).first()
	# print(data.get("tid"))
	if team is None:
		return JsonResponse({'error_code': 2, 'msg': "team not exist", "id": Team.objects.all().last().id, "tid":data.get("tid")})
	name = data.get('name')
	teacher = data.get('teacher')
	description = data.get('description')
	link = data.get('link')
	# TODO: change time
	startTime = data.get('startTime')
	endTime = data.get('endTime')
	startTime = datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
	endTime = datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
	# courseTime = CourseTime(addTime=addTime, endTime=endTime)
	# courseTime.save()

	image = data.get('image')
	print("this is image:\n"+image)
	course = Course(tid=team, name=name, teacher=teacher, description=description, link=link, picture=image)
	course.save()
	courseTime = CourseTime(startTime=startTime, endTime=endTime, cid=course)
	courseTime.save()
	return JsonResponse({'error_code': 0})


def is_joined(request):
	if request.method != "POST":
		return JsonResponse({'error_code': 1, 'msg': "not POST method"})
	data = json.loads(request.body)
	cs = CourseUser.objects.filter(cid=data.get("cid"), uid=data.get("uid")).first()
	if cs is None:
		return JsonResponse({"error_code": 0, "data": {"joined": 0}})
	else:
		return JsonResponse({"error_code": 0, "data": {"joined": 1}})


def join_course(request):
	if request.method != "POST":
		return JsonResponse({'error_code': 1, 'msg': "not POST method"})
	data = json.loads(request.body)
	cour = Course.objects.filter(id=data.get("cid")).first()
	user = User.objects.filter(id=data.get("uid")).first()
	if cour is None or user is None:
		return JsonResponse({"error_code": 1, "msg": "course or user not exist"})
	cs = CourseUser.objects.filter(cid=cour, uid=user).first()
	if cs is None:
		CourseUser.objects.create(cid=cour, uid=user)
		cour.student_num += 1
		cour.save()
		return JsonResponse({"error_code": 0, "data": {"joined": 1}})
	else:
		return JsonResponse({"error_code": 0, "data": {"joined": 0}})


def search_course(request):
	if request.method != "POST":
		return JsonResponse({'error_code': 1, 'msg': "not POST method"})
	data = json.loads(request.body)
	type = data.get("type")
	value = data.get("value")
	sort = data.get("sort")
	if type is None or value is None or sort is None:
		return JsonResponse({'error_code':2, 'msg': "wrong parameters"})
	result = []
	if sort==0:
		if type==0:
			courses = Course.objects.all()
			for course in courses:
				num = fuzz.token_sort_ratio(value, course.name)
				if num>40:
					result.append(get_simple_info(course))
		elif type==1:
			courses = Course.objects.filter(tid=int(value))
			for course in courses:
				result.append(get_simple_info(course))
		elif type==2:
			courses = CourseUser.objects.filter(uid=int(value))
			for ucourse in courses:
				course = ucourse.cid
				result.append(get_simple_info(course))
		else:
			return JsonResponse({'error_code': 3, 'msg': "wrong type value"})
	elif sort==1:
		if type == 0:
			courses = Course.objects.all().order_by("-course_time__startTime")
			for course in courses:
				num = fuzz.token_sort_ratio(value, course.name)
				if num > 40:
					result.append(get_simple_info(course))
		elif type == 1:
			courses = Course.objects.filter(tid=int(value)).order_by("-course_time__startTime")
			for course in courses:
				result.append(get_simple_info(course))
		elif type == 2:
			courses = CourseUser.objects.filter(uid=int(value)).order_by("-course_time__startTime")
			for ucourse in courses:
				course = ucourse.cid
				result.append(get_simple_info(course))
		else:
			return JsonResponse({'error_code': 3, 'msg': "wrong type value"})
	return JsonResponse({'error_code': 0, 'data': result})


def delete(request):
	if request.method != "POST":
		return JsonResponse({'error_code': 1, 'msg': "not POST method"})
	data = json.loads(request.body)
	id = data.get("id")
	course = Course.objects.filter(id=id).first()
	if course is None:
		return JsonResponse({'error_code': 2, 'msg': "course not exists"})
	course.delete()
	return JsonResponse({'error_code': 0, 'msg': "success"})
