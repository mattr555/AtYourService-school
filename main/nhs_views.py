from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseRedirect

from main.models import Group, SiteSettings

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
		'srv_min': settings.service_hours, 
		'led_min': settings.leadership_hours})

