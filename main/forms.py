from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from datetime import timedelta
from django.utils import timezone
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from main.models import UserEvent, UserProfile, Organization, Event, SiteSettings

import pytz
import string
import random

def grad_year_list():
    y = timezone.now().year
    if timezone.now().month >= 7:
        return [y+1, y+2, y+3, y+4]
    return [y, y+1, y+2, y+3]

class MyUserCreate(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    volunteer = forms.BooleanField(required=False)
    org_admin = forms.BooleanField(required=False)
    timezone = forms.ChoiceField(required=True, choices=[(i, i) for i in pytz.common_timezones])
    grad_class = forms.ChoiceField(required=True, choices=[(i, i) for i in grad_year_list()])
    member_status = forms.ChoiceField(required=True, choices=UserProfile.MEMBER_STATUSES)

    class Meta:
        fields = ('first_name', 'last_name', 'email', 'timezone', 'grad_class', 'member_status')
        model = User

    def save(self, commit=True):
        user = User.objects.create_user(self.cleaned_data['username'], self.cleaned_data['email'],
                                        self.cleaned_data['password1'])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.groups.add(Group.objects.get(name="Volunteer"))
        user.save()
        profile = UserProfile(user=user)
        profile.timezone = self.cleaned_data['timezone']
        profile.grad_class = int(self.cleaned_data['grad_class'])
        profile.membership_status = self.cleaned_data['member_status']
        profile.save()
        return user

class UserEventCreate(forms.ModelForm):
    date_start = forms.DateTimeField(required=True, widget=forms.DateTimeInput(format='%m/%d/%Y %I:%M %p'))
    date_end = forms.DateTimeField(widget=forms.DateTimeInput(format='%m/%d/%Y %I:%M %p'))

    class Meta:
        model = UserEvent
        fields = ('name', 'description', 'organization', 'advisor_email', 'date_start', 'date_end', 'location', 'hours_worked', 'hour_type')

    def __init__(self, user=None, *args, **kwargs):
        super(UserEventCreate, self).__init__(*args, **kwargs)
        self._user = user
        self._old_advisor_email = self.instance.advisor_email

    def save(self, commit=True):
        event = super(UserEventCreate, self).save(commit=False)
        event.user = self._user
        print(self._old_advisor_email)
        if self.cleaned_data.get('date_end') is None:
            event.date_end = event.date_start + timedelta(hours=event.hours_worked)
        if self._old_advisor_email != event.advisor_email:
            key = "".join([random.choice(string.ascii_letters) for i in range(20)])
            event.email_verification_key = key
            site = Site.objects.get_current()
            send_mail('{} has requested you to verify their service'.format(event.user.get_full_name()),
                      render_to_string('email/service_verify.txt', {'event': event, 'site': site, 'name': event.user.get_full_name()}),
                      'noreply@atyourservice.com',
                      [event.advisor_email])
        if commit:
            event.save()
        return event

    def clean_date_end(self):
        date_end = self.cleaned_data.get('date_end')
        date_start = self.cleaned_data.get('date_start')
        if date_start > date_end:
            raise forms.ValidationError("The start date should be before the end date!")
        return date_end

class UserEventVerify(forms.ModelForm):
    class Meta:
        model = UserEvent
        fields = ('advisor_email', 'advisor_name')

class EventCreate(forms.ModelForm):
    date_start = forms.DateTimeField(required=True, widget=forms.DateTimeInput(format='%m/%d/%Y %I:%M %p'))
    date_end = forms.DateTimeField(widget=forms.DateTimeInput(format='%m/%d/%Y %I:%M %p'))

    class Meta:
        model = Event
        fields = ('organization', 'name', 'description', 'location', 'date_start', 'date_end', 'geo_lat', 'geo_lon', 'hour_type')

    def __init__(self, user=None, *args, **kwargs):
        super(EventCreate, self).__init__(*args, **kwargs)
        self._user = user

    def save(self, commit=True):
        event = super(EventCreate, self).save(commit=False)
        event.organizer = self._user
        event.organization_id = self.cleaned_data.get('organization').id
        if commit:
            event.save()
        return event

    def clean_organization(self):
        org = self.cleaned_data.get('organization')
        if org.admin_id != self._user.id:
            raise forms.ValidationError("That's not your organization!")
        return org

    def clean_date_end(self):
        date_end = self.cleaned_data.get('date_end')
        date_start = self.cleaned_data.get('date_start')
        if date_start > date_end:
            raise forms.ValidationError("The start date should be before the end date!")
        return date_end

class OrganizationCreate(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('name', 'description', 'location', 'geo_lat', 'geo_lon')

    def __init__(self, user=None, *args, **kwargs):
        super(OrganizationCreate, self).__init__(*args, **kwargs)
        self._user = user

    def save(self, commit=True):
        o = super(OrganizationCreate, self).save(commit=False)
        o.admin = self._user
        if commit:
            o.save()
        return o

class NHSSettingsModify(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ('member_service_hours', 'candidate_service_hours', 'candidate_leadership_hours')

    def save(self, commit=True):
        settings = SiteSettings.objects.get(pk=1)
        settings.candidate_service_hours = self.cleaned_data['candidate_service_hours']
        settings.candidate_leadership_hours = self.cleaned_data['candidate_leadership_hours']
        settings.member_service_hours = self.cleaned_data['member_service_hours']
        if commit:
            settings.save()
        return settings

class SocialUserProf(forms.Form):
    timezone = forms.ChoiceField(choices=[(i, i) for i in pytz.common_timezones])
    grad_class = forms.ChoiceField(choices=[(i, i) for i in grad_year_list()])
    member_status = forms.ChoiceField(choices=[('MEM', 'NHS Member'), ('CAN', 'NHS Candidate')])
