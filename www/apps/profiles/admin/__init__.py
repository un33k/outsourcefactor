from django.contrib import admin

from ..models import UserProfile
from profile import UserProfileAdmin
admin.site.register(UserProfile, UserProfileAdmin)

from ..models import Skill, SkillSet
from skill import SkillAdmin, SkillSetAdmin
admin.site.register(Skill, SkillAdmin)
admin.site.register(SkillSet, SkillSetAdmin)

from ..models import JobPost
from job import JobPostAdmin
admin.site.register(JobPost, JobPostAdmin)