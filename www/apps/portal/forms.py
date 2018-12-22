from django import forms
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode

from www.apps.profiles.models import Skill, SkillSet, JobPost
from www.apps.profiles.forms import DeferredChoiceField, SkillSetForm
from www.apps.profiles.utils.countries import SORTED_COUNTRIES

class SearchTalentForm(forms.Form):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(SearchTalentForm, self).__init__(*args, **kwargs)
        self.fields['skill'].choices = [(0, 'Any')]
        self.fields['skill'].initial = 0 
        self.fields.keyOrder = [
            'category',
            'skill',
            'experience',
            'country',
            'last_activity',
            'keywords',
        ]
    category = [(c.id, c.name) for c in Skill.objects.get_categories()]
    category.insert(0, ('0', 'Any'))
    COUNTRY_CHOICES = [('', 'Any')] + SORTED_COUNTRIES

    # must follow the skill level in the skill model, we add (0, "Any") and handle is don't care
    SKILL_LEVEL_CHOICES = (
        (0, "Any"),
        (SkillSet.SKILL_LEVEL_BEGINNER, "Beginner or better"),
        (SkillSet.SKILL_LEVEL_JUNIOR, "Junior or better"),
        (SkillSet.SKILL_LEVEL_INTERMIDATE, "Intermediate or better"),
        (SkillSet.SKILL_LEVEL_EXPERIENCED, "Experienced or better"),
        (SkillSet.SKILL_LEVEL_EXPERT, "Expert"),
    )

    # DATE_1_WEEK_OR_LESS = 7
    # DATE_2_WEEKS_OR_LESS = 14
    DATE_1_MONTH_OR_LESS = 30
    DATE_3_MONTH_OR_LESS = 90
    DATE_6_MONTH_OR_LESS = 180
    DATE_1_YEAR_OR_LESS = 365
    DATE_CHOICES = (
        (0, "Any"),
        # (DATE_1_WEEK_OR_LESS, "1 week or less"),
        # (DATE_2_WEEKS_OR_LESS, "2 weeks or less"),
        (DATE_1_MONTH_OR_LESS, "1 month or less"),
        (DATE_3_MONTH_OR_LESS, "3 months or less"),
        (DATE_6_MONTH_OR_LESS, "6 months or less"),
        (DATE_1_YEAR_OR_LESS, "1 year or less"),
    )

    keywords = forms.CharField(
                max_length=56,
                required=False
    )
    
    category = forms.ChoiceField(
                choices=category,
                required=False
    )

    skill = DeferredChoiceField(
                choices=[],
                required=False
    )

    experience = forms.ChoiceField(
                choices=SKILL_LEVEL_CHOICES,
                required=False
    )

    country = forms.ChoiceField(
                choices=COUNTRY_CHOICES,
                required=False
    )
    
    last_activity = forms.ChoiceField(
                choices=DATE_CHOICES,
                required=False
    )

    def clean_keywords(self):
        keywords = self.cleaned_data.get('keywords', '')
        return keywords

    def clean_category(self):
        category = self.cleaned_data.get('category', 0)
        return category

    def clean_skill(self):
        skill = self.cleaned_data.get('skill', 0)
        return skill  

    def clean_experience(self):
        experience = self.cleaned_data.get('experience', 0)
        return experience  

    def clean_country(self):
        country = self.cleaned_data.get('country', '')
        return country

    def clean_last_activity(self):
        updated = self.cleaned_data.get('last_activity', 0)
        return updated

    def clean(self):
        category = self.clean_category()
        skill_id = self.clean_skill()
        skill_name_choice = []
        try:
            skill = Skill.objects.get(id=skill_id)
        except:
            skill = Skill({'id':0, 'name':'Any', 'category':None})
        
        if category:
            skill_name_choice = [(s.id, s.name) for s in Skill.objects.filter(category__exact=category)]
        
        skill_name_choice.insert(0, ('0', 'Any'))
        self.fields['skill'].choices = skill_name_choice
        self.fields['skill'].initial = skill.id     
        
        return self.cleaned_data

    class Meta:
        pass

# Job Search Form
class SearchJobForm(forms.Form):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(SearchJobForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'employment_option',
            'wage_salary',
            'posted_date',
            'keywords',
        ]

    JOB_OPTION_CHOICES = ((0, "Any"),) + JobPost.JOB_OPTION_CHOICES
    SALARY_WAGE_CHOICES = ((0, "Any"),) + JobPost.SALARY_WAGE_CHOICES

    # DATE_1_WEEK_OR_LESS = 7
    # DATE_2_WEEKS_OR_LESS = 14
    DATE_1_MONTH_OR_LESS = 30
    DATE_3_MONTH_OR_LESS = 90
    DATE_6_MONTH_OR_LESS = 180
    DATE_1_YEAR_OR_LESS = 365
    DATE_CHOICES = (
        (0, "Any"),
        # (DATE_1_WEEK_OR_LESS, "1 week or less"),
        # (DATE_2_WEEKS_OR_LESS, "2 weeks or less"),
        (DATE_1_MONTH_OR_LESS, "1 month or less"),
        (DATE_3_MONTH_OR_LESS, "3 months or less"),
        (DATE_6_MONTH_OR_LESS, "6 months or less"),
        (DATE_1_YEAR_OR_LESS, "1 year or less"),
    )

    keywords = forms.CharField(
                max_length=56,
                required=False
    )

    employment_option = forms.ChoiceField(
                choices=JOB_OPTION_CHOICES,
                required=False
    )
    
    wage_salary = forms.ChoiceField(
                choices=SALARY_WAGE_CHOICES,
                required=False
    )

    posted_date = forms.ChoiceField(
                choices=DATE_CHOICES,
                required=False
    )

    def clean_keywords(self):
        keywords = self.cleaned_data.get('keywords', '')
        return keywords

    def clean_employment_option(self):
        employment_option = self.cleaned_data.get('employment_option', 0)
        return employment_option

    def clean_wage_salary(self):
        wage_salary = self.cleaned_data.get('wage_salary', 0)
        return wage_salary

    def clean_posted_date(self):
        updated = self.cleaned_data.get('posted_date', 0)
        return updated

    class Meta:
        pass

# Business Search Form
class SearchBusinessForm(forms.Form):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(SearchBusinessForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'country',
            'keywords',
        ]

    COUNTRY_CHOICES = [('', 'Any')] + SORTED_COUNTRIES

    keywords = forms.CharField(
                max_length=56,
                required=False
    )

    country = forms.ChoiceField(
                choices=COUNTRY_CHOICES,
                required=False
    )

    def clean_keywords(self):
        keywords = self.cleaned_data.get('keywords', '')
        return keywords

    def clean_country(self):
        country = self.cleaned_data.get('country', '')
        return country

    class Meta:
        pass

