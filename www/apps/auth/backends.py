from django.contrib.auth.models import User, Permission
from django.contrib.auth.backends import ModelBackend as DjangoModelBackend
from django import forms

class ModelBackend(DjangoModelBackend):
    """ Authenticates user against username or email address"""

    # check if this is a valid email address
    def is_valid_email(self, email):
        emailfield = forms.EmailField()
        try:
            emailfield.clean(email)
            return True
        except forms.ValidationError:
            return False
        
    # check if this is a email-based authenticaiton
    def authenticate(self, username=None, password=None):
        # see if this is an email address
        try:
            if self.is_valid_email(username):
                user = User.objects.get(email__iexact=username)
            else:
                user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        
        return None
