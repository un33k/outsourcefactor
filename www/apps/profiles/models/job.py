import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import User
from uuslug import uuslug as slugify

class JobPost(models.Model):
    """
    Employer's job post
    """
    YES = 1
    NO = 2
    YES_NO_CHOICES = (
        (YES, 'Yes'),
        (NO, 'No'),
    )
    
    JOB_OPTION_FULL_TIME = 1
    JOB_OPTION_PART_TIME = 2
    JOB_OPTION_FREELANCE = 3
    JOB_OPTION_CHOICES = (
        (JOB_OPTION_FULL_TIME, 'Full-time'),
        (JOB_OPTION_PART_TIME, 'Part-time'),
        (JOB_OPTION_FREELANCE, 'Freelance'),
    )
    
    SALARY_WAGE_EXPERIENCE = 1
    SALARY_WAGE_NEGOTIABLE = 2
    SALARY_WAGE_10_100_USD = 3
    SALARY_WAGE_100_200_USD = 4
    SALARY_WAGE_200_300_USD = 5
    SALARY_WAGE_300_400_USD = 6
    SALARY_WAGE_400_500_USD = 7
    SALARY_WAGE_500_600_USD = 8
    SALARY_WAGE_600_700_USD = 9
    SALARY_WAGE_700_800_USD = 10
    SALARY_WAGE_800_900_USD = 11
    SALARY_WAGE_900_1000_USD = 12
    SALARY_WAGE_1000_1500_USD = 13
    SALARY_WAGE_1500_2000_USD = 14
    SALARY_WAGE_2000_3000_USD = 15
    SALARY_WAGE_3000_PLUS_USD = 16
    SALARY_WAGE_CHOICES = (
        (SALARY_WAGE_EXPERIENCE, 'Based on experience'),
        (SALARY_WAGE_NEGOTIABLE, 'Negotiable'),
        (SALARY_WAGE_10_100_USD, '10-100 USD'),
        (SALARY_WAGE_100_200_USD, '100-200 USD'),
        (SALARY_WAGE_200_300_USD, '200-300 USD'),
        (SALARY_WAGE_300_400_USD, '300-400 USD'),
        (SALARY_WAGE_400_500_USD, '400-500 USD'),
        (SALARY_WAGE_500_600_USD, '500-600 USD'),
        (SALARY_WAGE_600_700_USD, '600-700 USD'),
        (SALARY_WAGE_700_800_USD, '700-800 USD'),
        (SALARY_WAGE_800_900_USD, '800-900 USD'),
        (SALARY_WAGE_900_1000_USD, '900-1000 USD'),
        (SALARY_WAGE_1000_1500_USD, '1000-1500 USD'),
        (SALARY_WAGE_1500_2000_USD, '1500-2000 USD'),
        (SALARY_WAGE_2000_3000_USD, '2000-3000 USD'),
        (SALARY_WAGE_3000_PLUS_USD, '3000 + USD'),
    )
    
    user = models.ForeignKey(
                User,
                related_name="%(class)s",
                null=False
    )

    title = models.CharField(
                _('Job Title'), 
                blank=False, 
                max_length=56,
                help_text = _("Title of this job post (e.g. PHP developer, Marketing Manager)")
    )

    slug = models.CharField(
                _('Slug'), 
                blank=True, 
                max_length=200,
                help_text = _("Slug will be auto generated)")
    )
        
    description = models.TextField(
                _('Job Description'), 
                blank=False, 
                validators=[MinLengthValidator(25), MaxLengthValidator(750)],
                help_text = _("Detailed description of this jobs post")
    )


    requirements = models.TextField(
                _('Job Requirements'), 
                blank=True, 
                validators=[MinLengthValidator(25), MaxLengthValidator(750)],
                help_text = _("Detailed requirements for this job posts. (highly recommended)")
    )
    
    keywords = models.CharField(
                _('Related Keywords, Tags'), 
                blank=True,
                max_length=56,
                help_text = _("Job related keywords that makes the job easier to find. (e.g. English Wordpress HTML CSS PHP Article)")
    )
    
    contact = models.CharField(
                _('Job Contact Info'), 
                blank=True,
                max_length=56,
                help_text = _("Email or Number so jobseekers can contact you. OR leave blank to use your profile email")
    )
    
    employment_option = models.IntegerField(
                _('Employment Option'), 
                choices=JOB_OPTION_CHOICES, 
                blank=False,
                null=True,
                help_text = _("Full-time = dedicated stuff, Part-time = shared staff, Freelance = per project")
    )
    
    wage_salary = models.IntegerField(
                _('Salary'),
                choices=SALARY_WAGE_CHOICES, 
                blank=False,
                null=True,
                help_text = _("Monthly salary budget for this job")
    )
    
    start_date = models.DateField(
                _('Start Date'), 
                default=datetime.date.today(), 
                help_text = _("Start date. Select today for immediate start date -- format [YYYY-MM-DD]")
    )

    viewed = models.IntegerField(
                _('Number views'),
                default=0,
                help_text = _("How many people have viewed this job")
    )

    bookmarked = models.IntegerField(
                _('Number bookmarks'),
                default=0,
                help_text = _("How many people have bookmarked this job")
    )
        
    is_active = models.IntegerField(
                _('Active'),
                choices=YES_NO_CHOICES, 
                default=YES,
                help_text = _("Yes for active jobs.  No for hidden, non-active job posts")
    )
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        app_label = 'profiles'
        unique_together = (("user", "title"),)
        ordering = ['title',]


    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return "/job/%d/%s/" % (self.id, self.get_slug)
    
    @property
    def get_slug(self):
        return str(self.slug)

    @property
    def is_public(self):
        return self.is_active == self.YES

    @property
    def is_past_due(self):
        return datetime.date.today() >= self.start_date

    def just_viewed(self):
        self.viewed += 1
        self.save()
        return self.viewed
            
    def set_bookmark(self, increment=True):
        if increment:
            self.bookmarked += 1
        elif self.bookmarked > 0:
            self.bookmarked -= 1
        self.save()
        return self.bookmarked

    @property
    def is_complete(self):
        if self.title and self.description:
            return True
        return False
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title[:100])
        if not self.slug:
            self.slug = 'job' # ensure no empty slug
        p = self.user.get_profile()
        if p.is_employer:
            p.posted_jobs = True
            p.save()
        return super(JobPost, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        p = self.user.get_profile()
        if p.is_employer:
            j = JobPost.objects.filter(user=self.user)
            if len(j) <= 1: # this is the last job post, and it will be deleted right now
                p.posted_jobs = False
                p.save()
        return super(JobPost, self).delete(*args, **kwargs)




