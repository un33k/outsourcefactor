import time, string
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class SocialAuthProvider(models.Model):

    # binds to a user on this system
    user = models.ForeignKey(
                User,
                related_name="%(class)s",
                null=False
    )

    # provider choice
    name = models.CharField(
                _('Provider Name'),
                max_length=250,  
                null=False
    )

    # a unique universal identifier of this social account
    uuid = models.CharField(
                _('UUID'), 
                max_length=250, 
                null=False, 
                unique=True
    )

    # a unique email received from the social provider (not all provider emails)
    email = models.EmailField(
                _('Email'), 
                max_length=250, 
                null=False
    )
    
    # active flag on this provider
    is_active = models.BooleanField(
                _('Active'), 
                default=False
    )

    # book keeping
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        unique_together = (("user", "uuid"),('name', 'email'))
        ordering = ['user__username', 'uuid']

    def __unicode__(self):
            return u'%s-%s-%s' % (self.user.username, self.name, self.uuid)

    def save(self, *args, **kwargs):
        p = self.user.get_profile()
        p.save()
        return super(SocialAuthProvider, self).save(*args, **kwargs)


class SocialProfileProvider(models.Model):
    
    SOCIAL_SITE_YOUTUBE = 1
    SOCIAL_SITE_GITHUB = 2
    SOCIAL_SITE_BITBUCKET = 3
    SOCIAL_SITE_LINKEDIN = 4
    SOCIAL_SITE_FACEBOOK = 5
    SOCIAL_SITE_MYSPACE = 6
    SOCIAL_SITE_BLOGGER = 7
    SOCIAL_SITE_TWITTER = 8

    SOCIAL_SITE_CHOICES = (
        (SOCIAL_SITE_YOUTUBE,       'Youtube.com'),
        (SOCIAL_SITE_GITHUB,        'GitHub.com'),
        (SOCIAL_SITE_BITBUCKET,     'Bitbucket.org'),
        (SOCIAL_SITE_LINKEDIN,      'Linkedin.com'),
        (SOCIAL_SITE_FACEBOOK,      'Facebook.com'),
        (SOCIAL_SITE_MYSPACE,       'Myspace.com'),
        (SOCIAL_SITE_BLOGGER,       'Blogger.com'),
        (SOCIAL_SITE_TWITTER,       'Twitter.com'),
    )
    
    # user
    user = models.ForeignKey(
                User,
                related_name="%(class)s",
                null=False
    )
    
    # social networking provider
    provider = models.IntegerField(
                _('Website Type'),
                choices=SOCIAL_SITE_CHOICES,
                blank=False,
                null=True,
                help_text = _("Account Type")
    )
    
    # link to site 
    website = models.URLField(
                _('Website Link'), 
                max_length=100, 
                blank=True,
                help_text = _("Link to the website. Try URL in a browser first to ensure validity")
    )
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        unique_together = (("user", "provider"),)
        ordering = ['provider',]

    def __unicode__(self):
        return u'%s-%s' % (self.user.username, self.provider)

    def save(self, *args, **kwargs):
        p = self.user.get_profile()
        p.save()
        return super(SocialProfileProvider, self).save(*args, **kwargs)




