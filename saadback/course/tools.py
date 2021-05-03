

def get_simple_info(course):
	return {"id": course.id, "picture": course.picture, "name": course.name, "team": course.tid.name,
	        "teamid": course.tid.id, "description": course.description}