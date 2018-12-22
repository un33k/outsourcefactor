from django import template
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.template import Node, TemplateSyntaxError
from django.conf import settings
from ..models import SkillSet
register = template.Library()

@register.filter
def get_skills(user, skill_info):
    """
    Given a users object, and an arg in '#-#-#-#' for 'number-category-skill-level' format
    Retunrs the top N skills set by 'number' and filtered by category-skill-level' or returns None
    """
    skill_num = 3
    if not user.get_profile().is_employee:
        return None
    
    query = Q(**{"user": user})
    skills = SkillSet.objects.filter(query).order_by('skill__category__name', 'skill__name', '-level')
    if not skills:
        return None
    
    # did we receive some extra args to deal with?
    try:
        category = skill_info[0]
        skill = skill_info[1]
        level = skill_info[2]
    except:
        # failed to get the args, just send up the top N number of skills
        if len(skills) > skill_num:
            skills = skills[:skill_num]
        return skills

    # see if this is an exact skill filter, if so, deal with it, exact skill has to be on top
    c_q = None; s_q = None; l_q = None
    if category:
        c_q = Q(**{"skill__category": category})
    if skill:
        s_q = Q(**{"skill": skill})
    if level:
        l_q = Q(**{"level": level})

    if category and c_q:
        query = query & c_q
        if skill and s_q:
            query = query & s_q
        if level and l_q:
            query = query & l_q

    exact_skills = SkillSet.objects.filter(query).order_by('skill__category__name', 'skill__name', '-level')
    if exact_skills:
        if len(exact_skills) >= skill_num:
            skills = exact_skills[:skill_num] # exact search has enough, skills, so send it up
            return skills
    
        # add more skills equal to the skill_num
        exact_skills = list(exact_skills)
        for s in skills:
            if s not in exact_skills:
                exact_skills.append(s)
                if len(exact_skills) == skill_num:
                    skills = exact_skills
                    break
    else:
        skills = skills[:skill_num]
     
    return skills



