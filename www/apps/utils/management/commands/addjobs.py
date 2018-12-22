import os, datetime
from random import randint, choice
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from uuslug import uuslug
from django.conf import settings
from www.apps.profiles.models import *

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        if not getattr(settings, "DEBUG", True):
            return 
        users = User.objects.all()
        for u in users:
            if u.get_profile().is_employee:
                continue
        
            num = choice([2,3,4,5])
            for n in range(1, num):
                jp = JobPost()
                jp.user = u
                max_try = 0
                while True:
                    max_try += 1
                    jp.title = choice(["Lorem ipsum dolor sit amet consetetur sadipscing",
                                       "sed diam nonumy eirmod tempor",
                                       "invidunt ut labore et dolore magna",
                                       "aliquyam erat, sed diam voluptua At vero eos",
                                       "Senior PHP Developer & Webadmin",
                                       "English writer, Article writer",
                                       "Virtual assistance, fulltime",
                                       "Senior et accusam et justo duo dolores"])
                              
                    jp.description = choice(["Lorem ipsum dolor sit amet, "
                              "consetetur sadipscing elitr "
                              "sed diam nonumy eirmod tempor "
                              "invidunt ut labore et dolore magna "
                              "aliquyam erat, sed diam voluptua. "
                              "At vero eos et accusam et justo duo dolores", 
                              "Lorem ipsum dolor sit amet "
                              "consetetur sadipscing elitr "
                              "sed diam nonumy eirmod tempor ",
                              "Lorem ipsum dolor sit amet "
                              "consetetur sadipscing elitr"])
                    jp.requirements = choice(["Lorem ipsum dolor sit amet, "
                              "consetetur sadipscing elitr "
                              "sed diam nonumy eirmod tempor "
                              "invidunt ut labore et dolore magna "
                              "aliquyam erat, sed diam voluptua. "
                              "At vero eos et accusam et justo duo dolores", 
                              "Lorem ipsum dolor sit amet "
                              "consetetur sadipscing elitr "
                              "sed diam nonumy eirmod tempor ",
                              "Lorem ipsum dolor sit amet "
                              "consetetur sadipscing elitr"])
                    kw1=["wordpress", "graphic desiger", "artist", "virtual", "VA"]
                    kw2=["wordpress", "graphic desiger", "artist", "virtual", "VA"]
                    kw3=["wordpress", "graphic desiger", "artist", "virtual", "VA"]
                    kw4=["wordpress", "graphic desiger", "artist", "virtual", "VA"]
                    jp.keywords = choice(kw1) + " " + choice(kw2) + " " + choice(kw3) + " " + choice(kw4)
                    jp.employment_option = randint(1,len(JobPost.JOB_OPTION_CHOICES))
                    jp.wage_salary = randint(1,len(JobPost.SALARY_WAGE_CHOICES))
                    jp.start_date = datetime.date.today()
                    jp.viewed = choice([0, 1, 2,4,11,5,88,7,100, 1000])
                    jp.bookmarked = choice([0, 1, 2,4,11,5,88,7,100, 1000])
                    jp.is_active = choice([1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]) # way more YES=1 than NO=2
                    try:
                        jp.save()
                        break
                    except:
                        if max_try > 8:
                            break;
                self.stderr.write('created: %s, %s\n' % (u.username, jp.title))


