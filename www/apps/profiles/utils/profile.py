from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.humanize.templatetags.humanize import naturaltime
from www.apps.bookmark.models import Bookmark

from ..models import UserProfile
from job import update_employer_job_status
from skill import update_employee_skill_status
from ..utils.currency import get_to_usd_text

from www.apps.utils import *

def invalidate_profile_related_cache():
    delete_cache_access_key('Talent_Search_View')
    delete_cache_access_key('Job_Search_View')
    delete_cache_access_key('Business_Search_View')

def get_user_profile(user):
    """ Given a user object, it returns a user profile object """
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile
    
def update_user_profile(user):
    profile, created = UserProfile.objects.get_or_create(user=user)
    update_employer_job_status(profile)
    update_employee_skill_status(profile)
    return profile.save()

def get_user_as_employer_profile_and_dict_private(profile):
    """ get the employer profile information """
    pdict = []
    p = profile
    pdict.append({'lable': 'Contact name', 'value': p.full_name, 'help': 'Contact name for this business', })
    pdict.append({'lable': 'Country', 'value': p.get_country_display(), 'help': 'Country of operation for this business', })
    if p.website:
        pdict.append({'lable': 'Website', 'value': p.website, 'help': 'Business website', })
    pdict.append({'lable': 'Member since', 'value': naturaltime(p.user.date_joined), 'help': 'User joined on this date', })
    pdict.append({'lable': 'Last activity', 'value': naturaltime(p.user.last_login), 'help': 'User\'s last login', })
    return profile, pdict

def get_user_as_employer_profile_and_dict_public(profile):
    """ get the employer profile information """
    pdict = []
    p = profile
    # pdict.append({'lable': 'Contact name', 'value': p.full_name, 'help': 'Contact name for this business', })
    pdict.append({'lable': 'Country', 'value': p.get_country_display(), 'help': 'Country of operation for this business', })
    if p.website:
        pdict.append({'lable': 'Website', 'value': p.website, 'help': 'Business website', })
    pdict.append({'lable': 'Member since', 'value': naturaltime(p.user.date_joined), 'help': 'User joined on this date', })
    pdict.append({'lable': 'Last activity', 'value': naturaltime(p.user.last_login), 'help': 'User\'s last login', })
    return profile, pdict


def get_user_as_employee_profile_and_dict_private(profile):
    """ get the employee profile information, private """
    pdict = []
    p = profile
    pdict.append({'lable': 'Name', 'value': p.full_name, 'help': 'First name + last name', })
    pdict.append({'lable': 'Demographic', 'value': '%s, %s year old' % (p.get_gender_display(), p.get_age_display()), 'help': 'Gender & age group', })
    pdict.append({'lable': 'Country', 'value': p.get_country_display(), 'help': 'First name + last name', })
    pdict.append({'lable': 'Member since', 'value': naturaltime(p.user.date_joined), 'help': 'User joined on this date', })
    pdict.append({'lable': 'Last activity', 'value': naturaltime(p.user.last_login), 'help': 'User\'s last login', })
    pdict.append({'lable': 'Number of views', 'value': profile.viewed, 'help': 'Number of times profile was viewed', })
    pdict.append({'lable': 'Number of bookmarks', 'value': profile.bookmarked, 'help': 'Number of times profile was bookmarked', })
    return profile, pdict

def get_user_as_employee_profile_and_dict_public(profile):
    """ get the employee profile information, public """
    pdict = []
    p = profile
    pdict.append({'lable': 'Name', 'value': p.full_name, 'help': 'First name + last name', })
    pdict.append({'lable': 'Demographic', 'value': '%s, %s year old' % (p.get_gender_display(), p.get_age_display()), 'help': 'Gender & age group', })
    pdict.append({'lable': 'Country', 'value': p.get_country_display(), 'help': 'First name + last name', })
    pdict.append({'lable': 'Member since', 'value': naturaltime(p.user.date_joined), 'help': 'User joined on this date', })
    pdict.append({'lable': 'Last activity', 'value': naturaltime(p.user.last_login), 'help': 'User\'s last login', })
    
    return p, pdict

def get_user_profile_and_dict_private(profile):
    """ Return the profile based on employement type and visiblity """
    pdict = None
    if profile.is_employer:
        p, pdict = get_user_as_employer_profile_and_dict_private(profile)
    else:
        p, pdict = get_user_as_employee_profile_and_dict_private(profile)
    return profile, pdict

def get_user_profile_and_dict_public(profile):
    """ Return the profile based on employement type and visiblity """
    pdict = None
    if profile.is_employer:
        p, pdict = get_user_as_employer_profile_and_dict_public(profile)
    else:
        p, pdict = get_user_as_employee_profile_and_dict_public(profile)
    return profile, pdict


def get_user_contact_dict(profile):
    """ get user contact information """
    contact_dict = []
    
    contact_privacy = 'Private'
    if profile.is_employee:
        contact_privacy = 'Only viewable by logged-in members'

    contact_dict.append({
        'lable': 'Email', 
        'value': profile.user.email, 
        'help': 'Primary contact email address. [%s]' % contact_privacy, 
    })
    return contact_dict

def get_employment_profile_and_dict_public(profile):
    """ get the employment profile information """
    employment = None
    employment_dict = None
    if profile.is_employee:
        fields = [
            'is_available',
            'is_freelance', 
            'employment_option', 
            'hours_per_week', 
            'work_arrangements',
        ]
        employment_dict = model_to_dict(profile, fields=fields)
        if profile.desired_salary and profile.currency:
            employment_dict.append({
                    'lable': 'Desired monthly salary', 
                    'value': get_to_usd_text(profile.desired_salary, profile.currency), 
                    'help': 'Your monthly salary expectations for the total number of work hours per month. '
                            'Example, you want to work 20 hours per week for an employer, which would be equal to 80 hours per month. '
                            'So what would be your monthly salary expectations for 80 hours of work per month. '
                            'Please be realistic with your expecations. You should know what you are worth as employers expect you to know that.', 
            })
        if profile.is_available:
            employment_dict.append({
                        'lable': 'Availability date', 
                        'value': 'Immediately' if profile.is_past_due else profile.availability_date, 
                        'help': 'Date of availability. How soon can you start?', 
                })
    return profile, employment_dict

def get_employment_profile_and_dict_private(profile):
    """ get the employment profile information """
    employment = None
    employment_dict = None
    if profile.is_employee:
        fields = [
            'is_available',
            'is_freelance', 
            'employment_option', 
            'availability_date', 
            'hours_per_week', 
            'work_arrangements',
        ]
        employment_dict = model_to_dict(profile, fields=fields)
        if profile.desired_salary and profile.currency:
            employment_dict.append({
                    'lable': 'Desired monthly salary', 
                    'value': get_to_usd_text(profile.desired_salary, profile.currency), 
                     'help': 'Your monthly salary expectations for the total number of work hours per month. '
                             'Example, you want to work 20 hours per week for an employer, which would be equal to 80 hours per month. '
                             'So what would be your monthly salary expectations for 80 hours of work per month. '
                             'Please be realistic with your expecations. You should know what you are worth as employers expect you to know that.',
            })
    return profile, employment_dict

def bookmark_profile(user, profile):
    """ Bookmark a profile for user """
    bookmark = Bookmark.objects.create_bookmark(user, profile)
    return bookmark
 
def get_profile_bookmarks(user):
    """ get all profile bookmarks for user """
    bookmarks = Bookmark.objects.get_all_bookmarks_for_this_model_for_this_user(user, UserProfile)
    return bookmarks
   
def del_profile_bookmark(user, profile):
    """ delete a profile bookmark for this user """
    Bookmark.objects.delete_bookmark(user, profile)
    return


    