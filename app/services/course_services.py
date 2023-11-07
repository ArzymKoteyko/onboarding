from random import randint

from database.models import CourseTag, Course
from .common_services import *

def compute_tag(tag: CourseTag):
    res = {
        "type": CourseTag.obligation.name
    }
    if tag == CourseTag.obligation:
        res["content"] = "Обязательно",
        res["image"] = "icons/important.jpg"
    if tag == CourseTag.deadline:
        res["content"] = f"{randint(2,3)} недели",
        res["image"] = "icons/clock.jpg"
    return res

def compute_percentage():
    return randint(0,100)

def compute_course(course: Course):
    res = partition_to_dict(course)
    res["tags"] = [compute_tag(tag) for tag in res["tags"]]
    res["percentage"] = compute_percentage()
    res["created"] = str(res["created"])
    return res