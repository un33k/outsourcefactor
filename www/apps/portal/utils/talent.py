import re, datetime
from django.contrib.auth.models import User
from django.db.models import Q
from www.apps.profiles.models import UserProfile, SkillSet
from common import *

# we are interested in these related fields for an employee (skill) search
def get_employee_related_fields():
    up_fields = ['userprofile__'+f.name for f in UserProfile._meta.fields]
    ss_fields = ['skillset__'+f.name for f in SkillSet._meta.fields]
    sk_fields = ['skillset__skill_id', 
                 'skillset__skill__name', 
                 'skillset__skill__category', 
                 'skillset__skill__category__id', 
                 'skillset__skill__category__name', 
                 'skillset__detail']
    
    # manually add 
    return up_fields + ss_fields + sk_fields

# we text search within these fields for an employee search
def get_employee_text_search_fields():
    fields = [
        # UserProfile
        'userprofile__full_name', 
        'userprofile__about',
        
        # Employement
        'userprofile__title', 

        # SkillSet
        'skillset__skill__name',
        'skillset__skill__category__name',
        'skillset__detail',
    ]
    return fields

# query against user skill
def get_skillset_query(category=0, skill=0, level=0):
    query = None
    
    # get a query for category
    category = get_integer(category)
    if category:
        query = Q(**{"skillset__skill__category": category})
    
    # if we are given a skill, this is a narrow search, so forget about the category
    skill = get_integer(skill)
    if skill:
        query = Q(**{"skillset__skill": skill})
        
    # skill level only makes sense if we have a skill or at least a category
    if query:
        level = get_integer(level)
        if level:
            query = query & Q(**{"skillset__level__gte": level})
    
    return query

# query against user skill, if at least one skills is posted
def employee_has_posted_skills_query():
    query = Q(**{"userprofile__posted_skills": True})
    return query

# query against user's job post, if at the user is active
def employee_status_is_active_query():
    query = Q(**{"userprofile__account_status": UserProfile.ACCOUNT_STATUS_ACTIVE})
    return query

# query if user is an employee or an employer
def get_employee_type_query():
    return Q(**{"userprofile__employment_type": UserProfile.EMPLOYMENT_TYPE_EMPLOYEE})

# query by country
def get_talent_country_query(country):
    if not country:
        return None
    return Q(**{"userprofile__country": country})

# query against user last activity
def get_user_last_activity_date_query(update=0):
    query = None
    update = get_integer(update)
    if update:
        update = (datetime.date.today() - datetime.timedelta(update))
        query = Q(**{"last_login__gte": update.isoformat()})
    return query

# query if user is an employer
def get_employee_query(request, data):
    qlist = []

    # only search the emplyee's list
    employee_query = get_employee_type_query()
    qlist.append(employee_query)

    # only search active profiles
    account_status_query = employee_status_is_active_query()
    qlist.append(account_status_query)
    
    # only search for completed profiles
    completed_profile_query = get_completed_profile_query()
    qlist.append(completed_profile_query)

    # only search for specific country
    country = data.get('country', '')
    country_query = get_talent_country_query(country)
    qlist.append(country_query)

    #prepare for search by keywords
    keywords = data.get('keywords', '')
    if keywords:
        keywords_query = get_query(keywords, get_employee_text_search_fields())
        if keywords_query:
            qlist.append(keywords_query)
    
    # user must have at least one skill posted
    posted_skills = employee_has_posted_skills_query()
    if posted_skills:
        qlist.append(posted_skills)
    
    # prepare for filter by skill, category and level
    skill_category = data.get('category', 0)
    skill_skill = data.get('skill', 0)
    skill_experience = data.get('experience', 0)
    skill_query = get_skillset_query(skill_category, skill_skill, skill_experience)
    if skill_query:
        qlist.append(skill_query)

    #prepare for filter by 'up'date
    last_activity = data.get('last_activity', 0)
    date_query = get_user_last_activity_date_query(last_activity)
    if date_query:
        qlist.append(date_query)

    # stack up the queries
    query = None
    for q in qlist:
        if q:
            if query:
                query = query & q
            else:
                query = q

    return query, [skill_category, skill_skill, skill_experience, country]

# return employee profile list based on query
def get_employee_profile_list(query):
    # search
    related_fields = get_employee_related_fields()
    users = User.objects.select_related(*related_fields).filter(query)
    employee_list = UserProfile.objects.filter(user__in=users).order_by('-user__last_login', 'bookmarked', 'viewed', 'updated_at', 'full_name') 
    return employee_list







