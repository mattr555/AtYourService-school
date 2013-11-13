from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from main.models import Group, SiteSettings
from main.forms import NHSSettingsModify

@login_required
def nhs_home(request):
	if request.user.has_perm('auth.can_view'):
		return render(request, 'main/nhs_home.html')
	else:
		messages.error(request, 'You don\'t have permission to do that!')
		return HttpResponseRedirect('/')

@permission_required('auth.can_view', login_url='/forbidden')
def nhs_list(request):
	students = Group.objects.get(name='Volunteer').user_set.all()
	settings = SiteSettings.objects.get(pk=1)
	return render(request, 'main/nhs_list.html', {'students': students, 
		'srv_can_min': settings.candidate_service_hours, 
		'led_can_min': settings.candidate_leadership_hours,
		'srv_mem_min': settings.member_service_hours})

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
	
