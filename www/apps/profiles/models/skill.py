from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import User

class SkillManager(models.Manager):
    default_name = "general"
    
    def get_query_set(self):
        return super(SkillManager, self).get_query_set().order_by('priority', 'name')

        
    def get_default_name(self):
        return self.default_name

    def get_categories(self):
        return self.filter(category__isnull=True).order_by('priority', 'name')

    def get_default_category(self):
        try:
            return self.get(category__isnull=True, name__iexact=self.default_name)
        except:
            return None

    def get_category_skills(self, category):
        return self.filter(category__name__iexact=category).order_by('priority', 'name')

    def get_default_skill_for_category(self, category):
        try:
            return self.get(category__name__iexact=category, name__iexact=self.default_name)
        except:
            return None


class Skill(models.Model):
    """
    Skill name and its parent category
    """
    name = models.CharField(
                _('Skill Name'),
                max_length=70,
                null=False
    )

    category = models.ForeignKey(
                'self',
                blank=True,
                null=True
    )

    priority = models.IntegerField(
                _('Priority'), 
                default=100,
                help_text = _("A way to show the high priority skills first")
    )

    is_active = models.BooleanField(
                default=True
    )

    objects = SkillManager()

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        app_label = 'profiles'
        ordering = ['category__name', 'name']


    def __unicode__(self):
        return u'%s' % (self.name)


class SkillSet(models.Model):
    """
    User skill with its level & user experience detail
    """
    SKILL_NUM_DETAIL_REQRD  = 5 # detail is required on the first 5 skills
    SKILL_NUM_MAX_ALLOWED   = 10 # max number of allowed skills
    SKILL_LEVEL_BEGINNER    = 1
    SKILL_LEVEL_JUNIOR      = 2
    SKILL_LEVEL_INTERMIDATE = 3
    SKILL_LEVEL_EXPERIENCED = 4
    SKILL_LEVEL_EXPERT      = 5
    SKILL_LEVEL_CHOICES = (
        (SKILL_LEVEL_BEGINNER,      'Beginner - Never done it before, just started learning'),
        (SKILL_LEVEL_JUNIOR,        'Junior - Barely done it before, not quite comfortable'),
        (SKILL_LEVEL_INTERMIDATE,   'Intermediate - Comfortable at it, lack the experience'),
        (SKILL_LEVEL_EXPERIENCED,   'Experienced - Very comfortable at it, been doing it for a while'),
        (SKILL_LEVEL_EXPERT,        'Expert - Extremely comfortable at it, looking beyond my comfort zone'),
    )

    user = models.ForeignKey(
                User,
                related_name="%(class)s",
                null=False
    )

    skill = models.ForeignKey(
                'Skill', 
                null=False
    )
    
    level = models.IntegerField(
                _('Skill Level'), 
                choices=SKILL_LEVEL_CHOICES, 
                blank=False,
                null=False,
                help_text = _("Tell others about your level of experience with this skill")
    )

    detail = models.TextField(
                _('Skill Detail'), 
                blank=True, 
                validators=[MinLengthValidator(25), MaxLengthValidator(400)],
                help_text = _("Detail is required for your first %d skills, however we recommend it for all your skills" % SKILL_NUM_DETAIL_REQRD)
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'profiles'
        unique_together = (("user", "skill"),)
        ordering = ['skill__category__name', 'skill__name']


    def __unicode__(self):
        if self.skill.category:
            return u'%s-%s-%s' % (self.skill.category, self.skill.name, self.SKILL_LEVEL_CHOICES[self.level-1][1])
        else:
            return u'%s-%s' % (self.skill.name, self.SKILL_LEVEL_CHOICES[self.level-1][1])
            
    def save(self, *args, **kwargs):
        p = self.user.get_profile()
        if p.is_employee:
            p.posted_skills = True
            p.save()
        return super(SkillSet, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        p = self.user.get_profile()
        if p.is_employee:
            s = SkillSet.objects.filter(user=self.user)
            if len(s) <= 1: # this is the last skill set, and it will be deleted right now
                p.posted_skills = False
                p.save()
        return super(SkillSet, self).delete(*args, **kwargs)




