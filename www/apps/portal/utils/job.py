import re, datetime
from django.contrib.auth.models import User
from django.db.models import Q
from www.apps.profiles.models import JobPost, UserProfile
from common import *

# we text search within these fields for a job
def get_jobpost_text_search_fields():
    fields = [
        'title',
        'description',
        'keywords',
    ]
    return fields

# query against job post, if it is active
def jobpost_status_is_active_query():
    query = Q(**{"is_active": JobPost.YES})
    return query

# query against jobpost option
def get_jobpost_option_query(employment_option=0, wage_salary=0):
    query = None
    
    # get a query for employment_option
    employment_option = get_integer(employment_option)
    if employment_option:
        query = Q(**{"employment_option": employment_option})
    
    # get a query based on salary
    wage_salary = get_integer(wage_salary)
    if wage_salary:
        if query:
            query = query & Q(**{"wage_salary": wage_salary})
        else:
            query = Q(**{"wage_salary": wage_salary})

    return query

# query against jobpost creation date
def get_jobpost_date_query(update=0):
    query = None
    update = get_integer(update)
    if update:
        update = (datetime.date.today() - datetime.timedelta(update))
        query = Q(**{"created_at__gte": update.isoformat()})
    return query

# query job post
def get_jobpost_query(request, data):
    qlist = []

    # only search active jobs, jobs cannot be submitted unless complete
    jobpost_active_query = jobpost_status_is_active_query()
    qlist.append(jobpost_active_query)

    #prepare for search by keywords
    keywords = data.get('keywords', '')
    if keywords:
        keywords_query = get_query(keywords, get_jobpost_text_search_fields())
        if keywords_query:
            qlist.append(keywords_query)

    # prepare for filter by skill, category and level
    employment_option = data.get('employment_option', 0)
    wage_salary = data.get('wage_salary', 0)
    job_query = get_jobpost_option_query(employment_option, wage_salary)
    if job_query:
        qlist.append(job_query)

    #prepare for filter by 'up'date
    posted_date = data.get('posted_date', 0)
    date_query = get_jobpost_date_query(posted_date)
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

    return query, [employment_option, wage_salary]

# return jobpost list based on query
def get_jobpost_list(query):
    # search
    users = UserProfile.objects.filter(account_status=UserProfile.ACCOUNT_STATUS_ACTIVE, 
                        filled_in=True, employment_type=UserProfile.EMPLOYMENT_TYPE_EMPLOYEE)
    jobpost_list = JobPost.objects.filter(user__in=users).filter(query).order_by('viewed', 'bookmarked', 'updated_at', 'title') 
    return jobpost_list



