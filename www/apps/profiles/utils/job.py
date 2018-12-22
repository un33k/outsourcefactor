from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from www.apps.bookmark.models import Bookmark

from ..models import JobPost

def get_employer_jobpost(profile):
    """  """
    jobs = None
    if profile.is_employer:
        jobs = JobPost.objects.filter(user=profile.user).order_by('title', 'employment_option', 'is_active')
    return jobs

def get_employer_jobpost_public_view(profile):
    """ Returns all jobs post if profile is active and an employer """
    jobs = None
    if profile.is_enabled:
        jobs = get_employer_jobpost(profile)
    return jobs

def update_employer_job_status(profile):
    if profile.is_employer:
        jobs = JobPost.objects.filter(user=profile.user)
        if jobs:
            profile.posted_jobs = True
        else:
            profile.posted_jobs = False
        profile.save()

def bookmark_job(user, job):
    """ Bookmark a job for user """
    bookmark = Bookmark.objects.create_bookmark(user, job)
    return bookmark
 
def get_job_bookmarks(user):
    """ get all job bookmarks for user """
    bookmarks = None
    try:
        bookmarks = Bookmark.objects.get_all_bookmarks_for_this_model_for_this_user(user, JobPost)
    except:
        pass
    return bookmarks
   
def del_job_bookmark(user, job):
    """ delete a job bookmark for this user """
    Bookmark.objects.delete_bookmark(user, job)
    return 



