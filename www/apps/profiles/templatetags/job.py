from django import template
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.template import Node, TemplateSyntaxError
from django.conf import settings
from ..utils.currency import get_to_usd_text
from ..models import JobPost

register = template.Library()

@register.filter
def get_jobs(user, job_info):
    """
    Given a users object, and an arg in '#-#' for 'employment_option-wage_salary' format
    Retunrs the top N JobPost by 'number' and filtered by employment_option-wage_salary' or returns None
    """
    job_num = 3
    if not user.get_profile().is_employer:
        return None
    
    query = Q(**{"user": user}) & Q(**{"is_active": JobPost.YES})
    jobs = JobPost.objects.filter(query).order_by('employment_option', 'wage_salary')
    if not jobs:
        return None
    
    # did we receive some extra args to deal with?
    try:
        employment_option = job_info[0]
        wage_salary = job_info[1]
    except:
        # failed to get the args, just send up the top N number of jobs
        if len(jobs) > job_num:
            jobs = jobs[:job_num]
        return jobs

    # see if this is an exact job filter, if so, deal with it, exact jobs has to be on top
    o_q = None; w_q = None
    if employment_option:
        c_q = Q(**{"employment_option": employment_option})
    if wage_salary:
        w_q = Q(**{"wage_salary": wage_salary})

    if employment_option and o_q:
        query = query & o_q
    if wage_salary and w_q:
        query = query & w_q

    exact_jobs = JobPost.objects.filter(query).order_by('employment_option', 'wage_salary')
    if exact_jobs:
        if len(exact_jobs) >= job_num:
            jobs = exact_jobs[:job_num] # exact search has enough, jobs, so send it up
            return jobs
    
        # add more jobs equal to the job_num
        exact_jobs = list(exact_jobs)
        for j in jobs:
            if j not in exact_jobs:
                exact_jobs.append(j)
                if len(exact_jobs) == job_num:
                    jobs = exact_jobs
                    break
    else:
        jobs = jobs[:job_num]
     
    return jobs


@register.filter
def get_convert_currency(amount, from_cur):
    """
    given an amount, this tag converts it to USD dollar
    """
    return get_to_usd_text(amount, from_cur)

