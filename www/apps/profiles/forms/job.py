import datetime
from django import forms
from django.utils.translation import ugettext as _
from ..models import JobPost

class JobPostForm(forms.ModelForm):
    def __init__(self, request, obj=None, *args, **kwargs):
        self.request = request
        self.obj = obj
        super(JobPostForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['class'] = 'vDateFieldStartDate'
        self.fields['start_date'].initial=datetime.date.today()
        # self.fields.keyOrder = []

    class Meta:
        model = JobPost
        exclude = ('user', 'slug', 'viewed', 'bookmarked')

    def clean_title(self):
        try:
            jp = JobPost.objects.get(user=self.request.user, title__iexact=self.cleaned_data['title'])
        except:
            pass
        else:
            if jp != self.obj:
                #this is not an update, so don't allow duplicate job post to be created
                raise forms.ValidationError('You have already posted this job, choose a new title')
        
        return self.cleaned_data['title']

    def clean_is_active(self):
        available = self.cleaned_data.get('is_active')
        if available == JobPost.YES:
            date = self.cleaned_data.get('start_date')
            if not date:
                raise forms.ValidationError(
                            _("You need to set the start date.  Select today\'s date immediate start"))
            elif date < datetime.date.today():
                raise forms.ValidationError(_("Start date cannot be in the past!"))
        else:
            self.cleaned_data['start_date'] = datetime.date.today()
            
        return available
