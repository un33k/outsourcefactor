from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from ..models import SkillSet

def get_employee_skill(profile):
    """ Given an employee user, it returns an a list of skills for that employee """
    skills = None
    if profile.is_employee:
        skills = SkillSet.objects.filter(user=profile.user).order_by('-level', 'skill__category__name', 'skill__name')
    return skills

def get_employee_skill_public_view(profile):
    """ Given an employee user, it returns an a list of skills for that employee """
    skills = None
    if profile.is_enabled:
        skills = get_employee_skill(profile)
    return skills

def update_employee_skill_status(profile):
    if profile.is_employee:
        skills = SkillSet.objects.filter(user=profile.user)
        if skills:
            profile.posted_skills = True
        else:
            profile.posted_skills = False
        profile.save()
