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
        skill_list = Skill.objects.filter(category__isnull=False)
        users = User.objects.all()
        for u in users:
            if u.get_profile().is_employer:
                continue
        
            num = choice([1,2,3,4,5,6])
            max_try = 0
            for n in range(1, num):
                max_try += 1
                ss = SkillSet()
                ss.user = u
                while True:
                    ss.skill = choice(skill_list)
                    ss.level = randint(1,len(SkillSet.SKILL_LEVEL_CHOICES))
                    ss.detail = choice(["Lorem ipsum dolor sit amet, "
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
                    try:
                        ss.save()
                        break
                    except:
                        if max_try > 8:
                            break;
                self.stderr.write('created: %s, %s, %d\n' % (u.username, ss.skill.name, ss.level))


