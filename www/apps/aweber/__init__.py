from django.dispatch import receiver
from aweber.signals import user_verified
from aweber.utils import get_first_last_from_name

@receiver(user_verified)
def user_verified_callback(sender, **kwargs):
    user = kwargs['user']
    if user:
        profile = user.get_profile()
        segment = ''
        try:
            segment = kwargs['request'].session['aweber_data']['segment']
            if segment == 'employer':
                profile.employment_type = profile.EMPLOYMENT_TYPE_EMPLOYER
            elif segment == 'jobseeker':
                profile.employment_type = profile.EMPLOYMENT_TYPE_EMPLOYEE
        except:
            pass
            
        try:
            name = kwargs['request'].session['aweber_data']['name']
            profile.first_name, profile.last_name = get_first_last_from_name(name)
        except:
            pass
            
        profile.save()

