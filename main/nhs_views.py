from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect

@login_required
def nhs_home(request):
	if request.user.has_perm('auth.can_view'):
		return render(request, 'main/nhs_home.html')
	else:
		messages.error(request, 'You don\'t have permission to do that!')
		return HttpResponseRedirect('/')
