import datetime, string
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from uuslug import uuslug as slugify
from ..utils.countries import SORTED_COUNTRIES
from ..utils.currency import SORTED_CURRENCIES

class UserProfile(models.Model):
    """
    Each user gets a profile automatically.
    """
    
    YES = 1
    NO = 2
    YES_NO_CHOICES = (
        (YES, 'Yes'),
        (NO, 'No'),
    )

    AGE_16_18 = 1
    AGE_18_20 = 2
    AGE_20_25 = 3
    AGE_25_30 = 4
    AGE_30_35 = 5
    AGE_35_40 = 6
    AGE_40_45 = 7
    AGE_45_50 = 8
    AGE_50_55 = 9
    AGE_55_60 = 10
    AGE_60_PLUS = 11
    AGE_CHOICES = (
        (AGE_16_18, '16-18'),
        (AGE_18_20, '18-20'),
        (AGE_20_25, '20-25'),
        (AGE_25_30, '25-30'),
        (AGE_30_35, '30-35'),
        (AGE_35_40, '35-40'),
        (AGE_40_45, '40-45'),
        (AGE_45_50, '45-50'),
        (AGE_50_55, '50-55'),
        (AGE_55_60, '55-60'),
        (AGE_60_PLUS, '60+'),
    )
    
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
    )
    
    EMPLOYMENT_TYPE_EMPLOYEE = 1
    EMPLOYMENT_TYPE_EMPLOYER = 2
    EMPLOYMENT_TYPE_CHOICES = (
        (EMPLOYMENT_TYPE_EMPLOYEE, 'JobSeeker - You are looking for online jobs'),
        (EMPLOYMENT_TYPE_EMPLOYER, 'Employer - You are looking to hire talent'),
    )
    
    ACCOUNT_STATUS_ACTIVE = 1
    ACCOUNT_STATUS_DISABLED = 2
    ACCOUNT_STATUS_CHOICES = (
        (ACCOUNT_STATUS_ACTIVE, 'Active'),
        (ACCOUNT_STATUS_DISABLED, 'Hidden'),
    )
    
    WORK_OPTION_FULL_TIME = 1
    WORK_OPTION_PART_TIME = 2
    WORK_OPTION_CHOICES = (
        (WORK_OPTION_FULL_TIME, 'Full-time'),
        (WORK_OPTION_PART_TIME, 'Part-time'),
    )
    
    WORK_ARRANGEMENT_HOME_PERSONAL_COMPUTER = 1
    WORK_ARRANGEMENT_HOME_SHARED_COMPUTER = 2
    WORK_ARRANGEMENT_CAFE_PERSONAL_COMPUTER = 3
    WORK_ARRANGEMENT_CAFE_SHARED_COMPUTER = 4
    WORK_ARRANGEMENT_OFFICE_PERSONAL_COMPUTER = 5
    WORK_ARRANGEMENT_OFFICE_SHARED_COMPUTER = 6
    WORK_ARRANGEMENT_CHOICES = (
        (WORK_ARRANGEMENT_HOME_PERSONAL_COMPUTER, 'Work from home + Personal computer'),
        (WORK_ARRANGEMENT_HOME_SHARED_COMPUTER, 'Work from home + Shared computer'),
        (WORK_ARRANGEMENT_CAFE_PERSONAL_COMPUTER, 'Work from a cafe + Personal computer'),
        (WORK_ARRANGEMENT_CAFE_SHARED_COMPUTER, 'Work from a cafe + Shared computer'),
        (WORK_ARRANGEMENT_OFFICE_PERSONAL_COMPUTER, 'Work from an office + Personal computer'),
        (WORK_ARRANGEMENT_OFFICE_SHARED_COMPUTER, 'Work from an office + Shared computer'),
    )

    WORK_HOURS_MAX_5  = 1
    WORK_HOURS_MAX_10 = 2
    WORK_HOURS_MAX_15 = 3
    WORK_HOURS_MAX_20 = 4
    WORK_HOURS_MAX_25 = 5
    WORK_HOURS_MAX_30 = 6
    WORK_HOURS_MAX_35 = 7
    WORK_HOURS_MAX_40 = 8
    WORK_HOURS_MAX_40PLUS = 9
    
    WORK_HOURS_MAX_CHOICES = (
        (WORK_HOURS_MAX_5, '5 hours per week'),
        (WORK_HOURS_MAX_10, '10 hours per week'),
        (WORK_HOURS_MAX_15, '15 hours per week'),
        (WORK_HOURS_MAX_20, '20 hours per week'),
        (WORK_HOURS_MAX_25, '25 hours per week'),
        (WORK_HOURS_MAX_30, '30 hours per week'),
        (WORK_HOURS_MAX_35, '35 hours per week'),
        (WORK_HOURS_MAX_40, '40 hours per week'),
        (WORK_HOURS_MAX_40PLUS, '40+ hours per week'),
    )

    ACCOUNT_TIER_1 = 1
    ACCOUNT_TIER_2 = 2
    ACCOUNT_TIER_3 = 3
    ACCOUNT_TIER_4 = 4
    ACCOUNT_TIER_CHOICES = (
        (ACCOUNT_TIER_1, 'Tier One Services'),
        (ACCOUNT_TIER_2, 'Tier Two Services'),
        (ACCOUNT_TIER_3, 'Tier Three Services'),
        (ACCOUNT_TIER_4, 'Tier Four Services'),
    )

    NOTIFY_LEVEL_1 = 1
    NOTIFY_LEVEL_2 = 2
    NOTIFY_LEVEL_CHOICES = (
        (NOTIFY_LEVEL_1, 'Disable Notifications'),
        (NOTIFY_LEVEL_2, 'New Content, Training and Promotion Announcements (recommended)'),
    )

    # common
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    # profile for this user
    user = models.OneToOneField(User, related_name="%(class)s", unique=True)

    # common
    business = models.CharField(
                _("Business name"), 
                max_length=58, 
                blank=False,
                help_text = _("Name of your business to be published in your profile. (public)")
    )

    # common
    slug = models.CharField(
                _('Slug'), 
                blank=True, 
                max_length=200,
                help_text = _("Slug will be auto generated)")
    )
    
    # common
    first_name = models.CharField(
                _("First name"), 
                max_length=30, 
                blank=False,
                help_text = _("Your first name")
    )
    
    # common
    last_name = models.CharField(
                _("Last name"), 
                max_length=30, 
                blank=False, 
                help_text = _("Your last name (surname)")
    )

    # internal use
    full_name = models.CharField(
                _("Full name"), 
                max_length=200, 
                blank=True, 
                help_text = _("Your full name, first name + last name")
    )
    
    # common 
    website = models.URLField(
                _('Website'), 
                max_length=50, 
                blank=True,
                help_text = _("Business website. Try URL in a browser to ensure validity. (recommended)")
    )

    # common
    country = models.CharField(
                _('Country'),
                max_length=2,
                choices=SORTED_COUNTRIES,
                help_text = _("Name of the country you live in now")
    )
    
    # common
    about = models.TextField(
                _('About'), 
                blank=True, 
                validators=[MinLengthValidator(25), MaxLengthValidator(750)],
                help_text = _("Tell employers a little about yourself and the kind of job you want. (highly recommended)")
    )

    # hidden - profile type indicator, cannot be blank
    employment_type = models.IntegerField(
                _('Employment Type'), 
                choices=EMPLOYMENT_TYPE_CHOICES, 
                blank=False,
                null=True,
                help_text = _("Job Seeker if looking for work. Employer if looking to hire. Choose with care, cannot change later!")
    )
    
    # employee only
    age = models.IntegerField(
                _('Age'),
                choices=AGE_CHOICES,
                blank=False,
                null=True,
                help_text = _("Your age category")
    )


    # employee only
    gender = models.IntegerField(
                _('Gender'),
                choices=GENDER_CHOICES,
                blank=False,
                null=True,
                help_text = _("Male for man, Female for woman")
    )
    
    # employee only
    title = models.CharField(
                _('Professional Title'), 
                blank=False,
                max_length=68,
                help_text = _("Your next job title. Be specific so employers find you easily. e.g. Senior developer or Article Writer")
    )
    
    # employee only
    employment_option = models.IntegerField(
                _('Employment Option'), 
                choices=WORK_OPTION_CHOICES, 
                blank=False,
                null=True,
                help_text = _("Full time usually means 35+ hours per week and your only job")
    )

    # employee only
    is_freelance = models.IntegerField(
                _('Freelance'), 
                choices=YES_NO_CHOICES,
                default=NO,
                help_text = _("Are you available for freelance (per project) jobs?")
    )

    # employee only
    work_arrangements = models.IntegerField(
                _('Work Arrangements'), 
                choices=WORK_ARRANGEMENT_CHOICES, 
                default=WORK_ARRANGEMENT_HOME_PERSONAL_COMPUTER,
                help_text = _("If you have your own computer and location of your work")
    )

    # employee only
    hours_per_week = models.IntegerField(
                _('Maximum Availability'), 
                choices=WORK_HOURS_MAX_CHOICES, 
                default=WORK_HOURS_MAX_10,
                help_text = _("The maximum number of hours per week you want to work")
    )

    # employee only
    desired_salary = models.IntegerField(
                _('Desired Monthly Salary'),
                blank=False,
                null=True,
                help_text = _("Your desired (monthly) salary for your (total) work hours per month. Be realistic.")
    )
    
    # employee only
    currency = models.CharField(
                _('Desired Currency'),
                max_length=3,
                choices=SORTED_CURRENCIES,
                help_text = _("You prefer to get paid in this currency. (your local currency is recommended)")
    )
    
    # employee only
    availability_date = models.DateField(
                _('Availability Date'), 
                default=datetime.date.today(), 
                help_text = _("Date of availability. If available immediately, then select today -- format [YYYY-MM-DD]")
    )
    
    # employee only
    is_available = models.IntegerField(
                _('Actively looking for work'),
                choices=YES_NO_CHOICES, 
                default=YES,
                help_text = _("Choose yes, if actively looking for work. If so, then set the Availability Date also!")
    )

    # common
    account_status = models.IntegerField(
                _('Account Status'), 
                choices=ACCOUNT_STATUS_CHOICES, 
                default=ACCOUNT_STATUS_ACTIVE,
                help_text = _("Hidden accounts are not visible to others")
    )
    
    # common
    viewed = models.IntegerField(
                _('Number views'),
                default=0,
                help_text = _("How many people have viewed your profile")
    )
    
    # common
    bookmarked = models.IntegerField(
                _('Number bookmarks'),
                default=0,
                help_text = _("How many people have bookmarked your profile")
    )
    
    # employee only
    posted_skills = models.BooleanField(default=False)
    
    # employer only
    posted_jobs = models.BooleanField(default=False)

    # common
    filled_in = models.BooleanField(default=False)
        
    # employer only (hidden)
    tier = models.IntegerField(
                _('Tier'), 
                choices=ACCOUNT_TIER_CHOICES, 
                default=ACCOUNT_TIER_4,
                help_text = _("Tier for this account for applicable services")
    )

    # common (hidden)
    subscriptions = models.IntegerField(
                _('Email Subscriptions'), 
                choices=NOTIFY_LEVEL_CHOICES, 
                default=NOTIFY_LEVEL_2,
                help_text = _("Note: System level notifications are always sent to you.")
    )

    class Meta:
        app_label = 'profiles'

    def __unicode__(self):
        return u'%s' % (self.user.username)

    def get_absolute_url(self):
        if self.is_employer:
            return "/business/%d/%s/" % (self.id, self.get_slug)
        else:
            return "/jobseeker/%d/%s/" % (self.id, self.get_slug)

    @property
    def has_employment_type(self):
        return self.is_employee or self.is_employer
    
    @property
    def is_employee(self):
        return self.employment_type == self.EMPLOYMENT_TYPE_EMPLOYEE
    
    @property
    def is_employer(self):
        return self.employment_type == self.EMPLOYMENT_TYPE_EMPLOYER
    
    @property
    def is_enabled(self):
        # user's decision
        return self.account_status == self.ACCOUNT_STATUS_ACTIVE

    @property
    def get_slug(self):
        return str(self.slug)
    
    def get_full_name(self):
        full_name = u'%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    
    @property
    def is_complete(self):
        complete = False
        if self.is_employee:
            if self.full_name and self.title and self.posted_skills:
                complete = True
        elif self.is_employer:
            if self.full_name and self.business:
                complete = True
        return complete

    @property
    def is_publicly_viewable(self):
        # system's decision
        return self.filled_in and self.is_enabled

    def just_viewed(self):
        self.viewed += 1
        self.save()
        return self.viewed

    @property
    def is_past_due(self):
        return datetime.date.today() >= self.availability_date
        
    def set_bookmark(self, increment=True):
        if increment:
            self.bookmarked += 1
        elif self.bookmarked > 0:
            self.bookmarked -= 1
        self.save()
        return self.bookmarked

    def save(self, *args, **kwargs):
        # clean up the name and set full_name
        self.first_name = string.capwords(self.first_name)
        self.last_name = string.capwords(self.last_name)
        self.full_name = self.get_full_name()
        
        # fill in the slug
        if self.is_employer and self.business:
            self.slug = slugify(self.business[:100])
        elif self.is_employee and self.title:
            self.slug = slugify(self.title[:100])
        if not self.slug:
            self.slug = 'profile' # ensure no empty slug
            
        # see if profile is filled in
        self.filled_in = self.is_complete
        
        # superuser is the admin, always set it to employer
        if self.user.is_superuser:
            self.employment_type = self.EMPLOYMENT_TYPE_EMPLOYER
        
        # emails should be lower case all the times
        if self.user.email != self.user.email.lower():
            self.user.email = self.user.email.lower()
            self.user.save()
        
        # full time or part time, set based on avail time
        if self.hours_per_week >= self.WORK_HOURS_MAX_35:
            self.employment_option = self.WORK_OPTION_FULL_TIME
        else:
            self.employment_option = self.WORK_OPTION_PART_TIME
            
        return super(UserProfile, self).save(*args, **kwargs)



