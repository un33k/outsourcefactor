import os, datetime
from random import randint, choice
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from uuslug import uuslug
from django.conf import settings
from www.apps.profiles.models import *

class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    help = 'Add N number users'
    jobtitle1 = []
    jobtitle2 = []
    jobtitle3 = []
    
    def handle(self, *args, **options):
        if not getattr(settings, "DEBUG", True):
            return 
        # build job titles lists
        filename = os.path.join(os.path.dirname(__file__), '_jobtitles.txt')
        f = open(filename, 'r')
        jt = []
        for line in f.readlines():
            line = line.replace("\r|\n","").strip()
            if '=level1=' in line:
                jt = self.jobtitle1
                continue
            if '=level2=' in line:
                jt = self.jobtitle2
                continue
            if '=level3=' in line:
                jt = self.jobtitle3
                continue
            jt.append(line)
        f.close()
        
        # create users and profiles
        filename = os.path.join(os.path.dirname(__file__), '_usernames.txt')
        num = sum(1 for line in open(filename))
        f = open(filename, 'r')
        for line in f.readlines():
            line = line.replace("\r|\n","").strip()
            name = line.split('=')
            username = uuslug(name[0]).replace('-', '_')
            u, c = User.objects.get_or_create(username=username)
            u.first_name = name[0]
            u.last_name = name[1]
            u.email = username+'@neekman.com'
            u.save()
            u.set_password('val')
            u.save()
            p = u.get_profile()
            is_business = randint(1, num) % 2
            if is_business:
                p.business = u.last_name +" "+ u.first_name +" "+ choice(['Corporation', 'Inc.', 'Proprietorship', 'Limited'])
                p.country = choice(['CA', 'US', 'AU', 'NZ', 'GB'])
                p.website = choice(['http://', 'https://'])+choice(['yahoo.com', 'google.com', 'bing.com', 'rim.com', 'neekware.com'])
                p.employment_type = UserProfile.EMPLOYMENT_TYPE_EMPLOYER
            else:
                p.country = choice(['PH', 'PK', 'IN', 'BD'])
                p.employment_type = UserProfile.EMPLOYMENT_TYPE_EMPLOYEE

            p.first_name = u.first_name
            p.last_name = u.last_name
            p.gender = randint(1,len(UserProfile.GENDER_CHOICES))
            p.age = randint(1,len(UserProfile.AGE_CHOICES))
            p.web = choice(['PH', 'PK', 'IN', 'BD'])
            p.about = ("Lorem ipsum dolor sit amet, "
                      "consetetur sadipscing elitr, "
                      "sed diam nonumy eirmod tempor "
                      "invidunt ut labore et dolore magna "
                      "aliquyam erat, sed diam voluptua. "
                      "At vero eos et accusam et justo duo dolores")
            p.save()
            
            if not is_business:
                e = p
                e.title = choice(self.jobtitle1) + ' ' + choice(self.jobtitle2) + ' ' + choice(self.jobtitle3)
                e.employment_option = randint(1,len(UserProfile.WORK_OPTION_CHOICES))
                e.is_freelance = randint(1,len(UserProfile.YES_NO_CHOICES))
                e.work_arrangements = randint(1,len(UserProfile.WORK_ARRANGEMENT_CHOICES))
                e.hours_per_week = randint(1,len(UserProfile.WORK_HOURS_MAX_CHOICES))
                e.desired_salary = choice([1500, 2000, 8000, 10000, 15000, 20000, 400000, 60000, 100000])
                if p.country == 'PH':
                    e.currency = 'PHP'
                elif p.country == 'PK':
                    e.currency = 'PKR'
                elif p.country == 'IN':
                    e.currency = 'INR'
                elif p.country == 'BD':
                    e.currency = 'BDT'
                else:
                    e.currency = 'USD'
                e.availability_date = datetime.date.today()
                e.is_available = choice([1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]) # way more YES=1 than NO=2
                e.save()


            self.stderr.write('created: %s, %s\n' % (name[0], name[1]))
        f.close()
