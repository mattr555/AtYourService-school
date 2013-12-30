from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone

from itertools import chain
from operator import attrgetter

from main.models import Group, SiteSettings, User
from main.forms import NHSSettingsModify

@login_required
def nhs_home(request):
    if request.user.has_perm('auth.can_view'):
        return render(request, 'main/nhs_home.html')
    else:
        messages.error(request, 'You don\'t have permission to do that!')
        return HttpResponseRedirect('/')

@permission_required('auth.can_view', login_url='/forbidden')
def nhs_candidate_list(request):
    students = Group.objects.get(name='Volunteer').user_set.filter(user_profile__membership_status="CAN")
    settings = SiteSettings.objects.get(pk=1)
    return render(request, 'main/nhs_list.html', {'students': students, 
        'srv_can_min': settings.candidate_service_hours, 
        'led_can_min': settings.candidate_leadership_hours,
        'srv_mem_min': settings.member_service_hours,
        'student_type': 'Candidates'})

@permission_required('auth.can_view', login_url='/forbidden')
def nhs_member_list(request):
    students = Group.objects.get(name='Volunteer').user_set.filter(user_profile__membership_status="MEM")
    settings = SiteSettings.objects.get(pk=1)
    return render(request, 'main/nhs_list.html', {'students': students, 
        'srv_can_min': settings.candidate_service_hours, 
        'led_can_min': settings.candidate_leadership_hours,
        'srv_mem_min': settings.member_service_hours,
        'student_type': 'Members'})

@permission_required('auth.can_view', login_url='/forbidden')
def nhs_settings(request):
    settings = SiteSettings.objects.get(pk=1)
    if request.method == "POST":
        form = NHSSettingsModify(request.POST)
        if form.is_valid():
            settings = form.save()
            messages.success(request, 'Settings saved')
            return HttpResponseRedirect(reverse('main:nhs_home'))
    else:
        form = NHSSettingsModify(settings.__dict__)
        return render(request, 'main/nhs_settings.html', {'form': form})
    
@permission_required('auth.can_view', login_url='/forbidden')
def nhs_user_report(request, pk):
    volunteers = Group.objects.get(name='Volunteer').user_set
    user = get_object_or_404(volunteers, pk=pk)
    event = list(user.events.all())
    user_event = list(user.user_events.all())
    event_set = sorted(chain(event, user_event),
        key=attrgetter('date_end'))
    if user.user_profile.membership_status == 'CAN':
        return render(request, 'main/nhs_candidate_report.html', {'user': user,
            'events': event_set})

    this_month = timezone.datetime(timezone.now().year, timezone.now().month, 1)
    last_month_event = list(user.events.filter(date_start__gte=this_month - timezone.timedelta(months=1),
        date_start__lte=this_month))
    last_month_user_event = list(user.user_events.filter(date_start__gte=this_month - timezone.timedelta(months=1),
        date_start__lte=this_month))
    last_month_event_set = sorted(chain(last_month_event, last_month_user_event),
        key=attrgetter('date_end'))
    return render(request, 'main/nhs_member_report.html', {'user': user,
        'events': event_set,
        'last_month_events': last_month_event_set})

@permission_required('auth.can_view', login_url='/forbidden')
def change_org_admin(request, pk):
    user = get_object_or_404(User, pk=pk)
    group = Group.objects.get(name="Org_Admin")
    if user not in group.user_set.all():
        group.user_set.add(user)
    else:
        group.user_set.remove(user)
    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET.get('next'))
    return HttpResponseRedirect(reverse('main:nhs_list'))
