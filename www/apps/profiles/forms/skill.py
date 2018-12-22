from django import forms
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode

from ..models import Skill, SkillSet

class DeferredChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), required=True, widget=None, label=None,
                 initial=None, help_text=None, *args, **kwargs):
        super(DeferredChoiceField, self).__init__(required=required, widget=widget, label=label,
                                        initial=initial, help_text=help_text, *args, **kwargs)

    def valid_value(self, value):
        "Check to see if the provided value is a valid choice"
        for k, v in self.choices:
            if isinstance(v, (list, tuple)):
                # This is an optgroup, so look inside the group for options
                for k2, v2 in v:
                    if value == smart_unicode(k2):
                        return True
            else:
                if value == smart_unicode(k):
                    return True
        return True


class SkillSetForm(forms.ModelForm):
    def __init__(self, request, obj=None, *args, **kwargs):
        self.request = request
        self.obj = obj
        super(SkillSetForm, self).__init__(*args, **kwargs)
        if obj:
            # OK, we got an object in, so this must be an update, we need to recreate the
            # skill_category and skill_name which are not based on the SkillSet model
            skill = obj.skill
            self.fields['skill_category'].choices = self.categories
            self.fields['skill_category'].initial = skill.category.id
            skill_name_choice = [(s.id, s.name) for s in Skill.objects.filter(category__exact=skill.category)]
            self.fields['skill_name'].choices = skill_name_choice
            self.fields['skill_name'].initial = skill.id           
        self.fields.keyOrder = [
            'skill_category',
            'skill_name',
            'level',
            'detail'
        ]

    categories = [(c.id, c.name) for c in Skill.objects.get_categories()]

    skill_category = forms.ChoiceField(
                choices=categories,
                required=True,
                initial=categories[0],
                help_text = _("Skill category")
    )
    
    skill_name = DeferredChoiceField(
                choices=[],
                required=True,
                help_text = _("Skill name")
    )

    class Meta:
        model = SkillSet
        exclude = ('user', 'skill')

    def clean_skill_category(self):
        category = self.cleaned_data.get('skill_category', 0)
        return category

    def clean_skill_name(self):
        try:
            ss = SkillSet.objects.get(user=self.request.user, skill=self.cleaned_data['skill_name'])
        except:
            pass
        else:
            if ss != self.obj:
                # this is not an update, so don't allow duplicate skill to be created
                raise forms.ValidationError('You have already chosen this skill, choose a new skill')
        
        return self.cleaned_data['skill_name']

    # on the first SKILL_NUM_DETAIL_REQRD skill, user must provide a details description
    def clean_detail(self):
        num = SkillSet.objects.filter(user=self.request.user).count()
        if num < SkillSet.SKILL_NUM_DETAIL_REQRD:
            if not self.cleaned_data['detail']:
                raise forms.ValidationError('This field is required for your first %d skills' % SkillSet.SKILL_NUM_DETAIL_REQRD)
        
        return self.cleaned_data['detail']

    def clean(self):
        num = SkillSet.objects.filter(user=self.request.user).count()
        if num >= SkillSet.SKILL_NUM_MAX_ALLOWED:
            raise forms.ValidationError('You have already selected your top (%d) skills. Try to change or add more details to your top skills.' % SkillSet.SKILL_NUM_MAX_ALLOWED)

        category = self.clean_skill_category()
        if category:
            skills = Skill.objects.filter(category=category)
            self.fields['skill_name'].choices = [ (s.id, s.name) for s in skills ]

        return self.cleaned_data

    def save(self):
        if self.obj:
            ss = self.obj
        else:
            ss = SkillSet(user=self.request.user)
            
        ss.level = self.cleaned_data['level']
        ss.detail = self.cleaned_data['detail']
        ss.skill = Skill.objects.get(id=self.cleaned_data['skill_name'])
            
        return ss.save()


