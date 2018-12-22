import re, datetime
from django.contrib.auth.models import User
from django.db.models import Q
from www.apps.profiles.models import UserProfile
from common import *

# we text search within these fields for an business search
def get_business_text_search_fields():
    fields = [
        # UserProfile
        'userprofile__business', 
        'userprofile__website',
        'userprofile__about',
    ]
    return fields

# we are interested in these related fields for a business search
def get_business_related_fields():
    up_fields = ['userprofile__'+f.name for f in UserProfile._meta.fields]
    
    # manually add 
    return up_fields 

# query if at the user is active
def business_status_is_active_query():
    query = Q(**{"userprofile__account_status": UserProfile.ACCOUNT_STATUS_ACTIVE})
    return query
    
# query to ensure user is an business
def get_business_type_query():
    return Q(**{"userprofile__employment_type": UserProfile.EMPLOYMENT_TYPE_EMPLOYER})

# query by country
def get_business_country_query(country):
    if not country:
        return None
    return Q(**{"userprofile__country": country})

# query if user is a jobseeker
def get_business_query(request, data):
    qlist = []

    # only search the business's list
    business_query = get_business_type_query()
    qlist.append(business_query)

    # only search active profiles
    account_status_query = business_status_is_active_query()
    qlist.append(account_status_query)
    
    # only search for completed profiles
    completed_profile_query = get_completed_profile_query()
    qlist.append(completed_profile_query)

    # only search for specific country
    country = data.get('country', '')
    country_query = get_business_country_query(country)
    qlist.append(country_query)
        
    #prepare for search by keywords
    keywords = data.get('keywords', '')
    if keywords:
        keywords_query = get_query(keywords, get_business_text_search_fields())
        if keywords_query:
            qlist.append(keywords_query)

    # stack up the queries
    query = None
    for q in qlist:
        if q:
            if query:
                query = query & q
            else:
                query = q

    return query, [country]

# return businesss profile list based on query
def get_business_profile_list(query):
    # search
    related_fields = get_business_related_fields()
    users = User.objects.select_related(*related_fields).filter(query)
    business_list = UserProfile.objects.filter(user__in=users).order_by('viewed', 'bookmarked', 'updated_at') 
    return business_list



