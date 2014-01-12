from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.conf import settings

import random
import string
import pytz

from main.forms import MyUserCreate, SocialUserProf

def login_view(request):
    if request.user.is_authenticated():
        messages.error(request, 'You are already logged in')
        return HttpResponseRedirect(request.GET.get('next', '/'))
    if request.method == "POST":
        uname, pword = request.POST.get('uname'), request.POST.get('pword')
        user = authenticate(username=uname, password=pword)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'You have been logged in')
            else:
                return render(request, 'main/login.html', {'error_message': 'That user is inactive!'})
        else:
            return render(request, 'main/login.html', {'error_message': 'Incorrect username/password combo.'})
        return HttpResponseRedirect(request.GET.get('next', '/'))
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return HttpResponseRedirect('/')

def signup(request):
    if request.method == "POST":
        form = MyUserCreate(request.POST)
        if form.is_valid():
            u = form.save()
            messages.success(request, "User was created successfully. Please sign in.<br>A validation email was sent to the account you registered with.",
                             extra_tags="safe")
            key = "".join([random.choice(string.ascii_letters) for i in range(20)])
            u.user_profile.email_validation_key = key
            u.user_profile.save()
            site = Site.objects.get_current()
            try:
                send_mail('AtYourService Email Validation',
                          render_to_string('email/validation.txt', {'validation_key': key, 'site': site}),
                          'noreply@atyourservice.com',
                          [u.email])
            except:
                u.user_profile.email_valid = True
                u.user_profile.email_validation_key = ''
                u.user_profile.save()
            return HttpResponseRedirect('/')
        return render(request, 'main/signup.html', {'errors': form.errors, 'timezones': pytz.common_timezones, 'form': form})
    elif request.user.is_authenticated():
        messages.error(request, 'You are already logged in')
        return HttpResponseRedirect(request.GET.get('next', '/'))
    form = MyUserCreate()
    return render(request, 'main/signup.html', {'timezones': pytz.common_timezones, 'form': form})

@login_required
def change_location(request):
    if request.method == "POST":
        p = request.user.user_profile
        p.location = request.POST.get('location')
        p.geo_lat = request.POST.get('lat')
        p.geo_lon = request.POST.get('lon')
        p.save()
        messages.info(request, 'Location successfully added')
        if request.GET.get('next'):
            return HttpResponseRedirect(request.GET.get('next'))
        return HttpResponseRedirect(reverse('main:user_profile'))  # should be profile detail
    return render(request, 'main/location_pick.html')

@login_required
def user_profile(request):
    return render(request, 'main/user_profile.html')

def finish_change_pass(request):
    messages.success(request, 'Password reset successfully')
    return HttpResponseRedirect('/')

@login_required
def email_validation(request, key):
    profile = request.user.user_profile
    if not profile.email_valid:
        if key == profile.email_validation_key:
            profile.email_valid = True
            profile.email_validation_key = ""
            profile.save()
            messages.success(request, 'Email verified successfully')
        else:
            messages.error(request, 'That verification key is incorrect :/')
    else:
        messages.info(request, 'Your email is already valid!')
    return HttpResponseRedirect(reverse('main:user_profile'))

def social_user_new(request):
    if request.method == "POST":
        form = SocialUserProf(request.POST)
        if form.is_valid():
            request.session['saved_timezone'] = form.cleaned_data['timezone']
            request.session['saved_grad_class'] = form.cleaned_data['grad_class']
            request.session['saved_member_status'] = form.cleaned_data['member_status']
            backend = request.session['partial_pipeline']['backend']
            return redirect('social:complete', backend=backend)
        messages.error(request, 'Choose something valid.')
    return render(request, 'main/social_user_new.html', {'timezones': pytz.common_timezones})
