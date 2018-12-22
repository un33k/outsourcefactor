import datetime
from django import forms
from django.utils.translation import ugettext as _
from ..models import UserProfile

class UserProfileTypeSelectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileTypeSelectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserProfile
        fields = ('employment_type',)

class UserProfileCommonEmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileCommonEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['about'].label = _("About Me")

    class Meta:
        model = UserProfile
        fields = (
                'first_name',
                'last_name', 
                'age', 
                'gender', 
                'country', 
                'about',  
                'account_status',
        )

    def clean_firstname(self):
        firstname = self.cleaned_data.get('first_name')
        if len(firstname) < 2:
            raise forms.ValidationError(_("Name too short! minimum length is ")+" [%d]" % 2)

        return firstname

    def clean_lastname(self):
        lastname = self.cleaned_data.get('last_name')
        if len(lastname) < 2:
            raise forms.ValidationError(_("Last name too short! minimum length is ")+" [%d]" % 2)
        return lastname

class UserProfileEmployementEmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileEmployementEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['availability_date'].widget.attrs['class'] = 'vDateFieldAvailableDate'
        self.fields['availability_date'].initial=datetime.date.today()

    class Meta:
        model = UserProfile
        fields = (
                'title',
                'is_freelance', 
                'work_arrangements', 
                'hours_per_week', 
                'desired_salary', 
                'currency',  
                'availability_date',
                'is_available',
        )

    def clean_is_available(self):
        available = self.cleaned_data.get('is_available')
        if available == UserProfile.YES:
            date = self.cleaned_data.get('availability_date')
            if not date:
                raise forms.ValidationError(
                            _("You need to set the date of your availability.  Select today\'s date if available immediately"))
            elif date < datetime.date.today():
                raise forms.ValidationError(_("Date of availability cannot be in the past!"))
        else:
            self.cleaned_data['availability_date'] = datetime.date.today()
            
        return available

class UserProfileCommonEmployerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileCommonEmployerForm, self).__init__(*args, **kwargs)
        self.fields['about'].label = _("About Us")
        self.fields['about'].help_text = _("Tell others a little about your company. (highly recommended)")
        self.fields['country'].help_text = _("Name of the country your business in located in.")
        self.fields['first_name'].help_text = _("Your first name. (private)")
        self.fields['last_name'].help_text = _("Your last name. (private)")
        
    class Meta:
        model = UserProfile
        fields = (
                'business',
                'first_name',
                'last_name', 
                'website', 
                'country', 
                'about', 
                'account_status',
        )

    def clean_business(self):
        business = self.cleaned_data.get('business')
        if len(business) < 2:
            raise forms.ValidationError(_("Business name too short! minimum length is ")+" [%d]" % 2)
        return business

    def clean_firstname(self):
        firstname = self.cleaned_data.get('first_name')
        if len(firstname) < 2:
            raise forms.ValidationError(_("Name too short! minimum length is ")+" [%d]" % 2)
        return firstname

    def clean_lastname(self):
        lastname = self.cleaned_data.get('last_name')
        if len(lastname) < 2:
            raise forms.ValidationError(_("Last name too short! minimum length is ")+" [%d]" % 2)
        return lastname




