import datetime
from django.contrib.sitemaps import Sitemap
from django.db.models import Q
from django.contrib.flatpages.models import FlatPage
from www.apps.profiles.models import UserProfile, JobPost

class BusinessSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.4

    def items(self):
        # query if user is an employer
        query = self.get_query()
        return UserProfile.objects.filter(query).order_by('-updated_at') 
        
    def get_query(self):
        qlist = []

        # only search the emplyee's list
        employee_query = Q(**{"employment_type": UserProfile.EMPLOYMENT_TYPE_EMPLOYER})
        qlist.append(employee_query)

        # only search active profiles
        account_status_query = Q(**{"account_status": UserProfile.ACCOUNT_STATUS_ACTIVE})
        qlist.append(account_status_query)
    
        # only search for completed profiles
        completed_profile_query = Q(**{"filled_in": True})
        qlist.append(completed_profile_query)

        # stack up the queries
        query = None
        for q in qlist:
            if q:
                if query:
                    query = query & q
                else:
                    query = q
        return query

class JobseekerSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        # query if user is a jobseeker
        query = self.get_query()
        return UserProfile.objects.filter(query).order_by('-updated_at') 
        
    def get_query(self):
        qlist = []

        # only search the emplyee's list
        employee_query = Q(**{"employment_type": UserProfile.EMPLOYMENT_TYPE_EMPLOYEE})
        qlist.append(employee_query)

        # only search active profiles
        account_status_query = Q(**{"account_status": UserProfile.ACCOUNT_STATUS_ACTIVE})
        qlist.append(account_status_query)
    
        # only search for completed profiles
        completed_profile_query = Q(**{"filled_in": True})
        qlist.append(completed_profile_query)

        # stack up the queries
        query = None
        for q in qlist:
            if q:
                if query:
                    query = query & q
                else:
                    query = q
        return query


class JobSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        # query for jobs
        query = self.get_query()
        return JobPost.objects.filter(query).order_by('-updated_at') 
        
    def get_query(self):
        qlist = []

        # only search the emplyee's list
        employee_query = Q(**{"is_active": JobPost.YES})
        qlist.append(employee_query)

        # stack up the queries
        query = None
        for q in qlist:
            if q:
                if query:
                    query = query & q
                else:
                    query = q
        return query


