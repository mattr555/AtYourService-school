from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.conf import settings as dj_settings
from django.core.mail import EmailMultiAlternatives

from itertools import chain
from operator import attrgetter

from main.models import Group, SiteSettings, User, Demerit, Site
from main.forms import NHSSettingsModify

def send_html_mail(subject, plaintext, html, from_address, recipients):
    msg = EmailMultiAlternatives(subject, plaintext, from_address, recipients)
    msg.attach_alternative(html, 'text/html')
    msg.send()

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
    settings = SiteSettings.objects.get(pk=1)
    if user.user_profile.membership_status == 'CAN':
        return render(request, 'main/nhs_candidate_report.html', {'user': user,
            'events': event_set,
            'srv_min': settings.candidate_service_hours,
            'led_min': settings.candidate_leadership_hours})
    return render(request, 'main/nhs_member_report.html', {'user': user,
        'events': event_set,
        'srv_min': settings.member_service_hours})

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

@permission_required('auth.can_view', login_url='/forbidden')
def demerit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        if request.POST.get('reason'):
            d = Demerit(user=user, reason=request.POST.get('reason'))
            d.save()
            site = Site.objects.get(pk=1)
            plaintext = render_to_string('email/demerit.txt', {'reason': request.POST.get('reason'), 
                'SCHOOL_NAME': dj_settings.SCHOOL_NAME, 'SCHOOL_SHORT_NAME': dj_settings.SCHOOL_SHORT_NAME})
            html = render_to_string('email/demerit.html', {'reason': request.POST.get('reason'), 'site': site,
                'SCHOOL_NAME': dj_settings.SCHOOL_NAME, 'SCHOOL_SHORT_NAME': dj_settings.SCHOOL_SHORT_NAME})
            send_html_mail('[AtYourService] You\'ve been demerited!', plaintext, html, dj_settings.DEFAULT_FROM_EMAIL, (user.email,))
            messages.success(request, 'Demerit applied successfully')
            return HttpResponseRedirect(reverse('main:nhs_user_report', args=(str(user.id))))
        messages.error(request, 'Please enter a reason')
    return render(request, 'main/nhs_demerit.html', {'user': user})

@permission_required('auth.can_view', login_url='/forbidden')
def delete_demerit(request, pk):
    demerit = get_object_or_404(Demerit, pk=pk)
    demerit.delete()
    messages.info(request, 'Demerit successfully deleted')
    return HttpResponseRedirect(reverse('main:nhs_user_report', args=(str(demerit.user_id))))

@permission_required('auth.can_view', login_url='/forbidden')
def induct(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.user_profile.membership_status = 'MEM'
    user.user_profile.save()
    messages.success(request, 'User successfully promoted to member')
    return HttpResponseRedirect(reverse('main:nhs_user_report', args=(str(user.id))))
