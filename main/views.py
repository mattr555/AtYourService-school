from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.core.urlresolvers import reverse

from itertools import chain
from operator import attrgetter
from datetime import datetime

from main.forms import UserEventCreate, UserEventVerify
from main.models import Event, UserEvent, Organization

def home(request):
    return render(request, 'main/home.html')

def list_events_one(request):
    return list_events(request, 1)

def list_events(request, page):
    filter_dict, filters = {}, {}
    if request.GET.get('range'):
        if not request.user.is_anonymous():
            if request.user.user_profile.geo_lat:
                dist = request.GET.get('range')
                set = Event.objects.within(request.user.user_profile, float(dist))
                set = set.filter(date_start__gte=timezone.now()).order_by('date_start')
                if float(dist) == 1.0:
                    mi = ' mile'
                else:
                    mi = ' miles'
                filters['Search radius: ' + str(dist) + mi] = 'range=' + dist
            else:
                messages.error(request, "You don't have a location set! <a href='/profile/change_loc?next=" + reverse('main:list_events') + "'>Set one now</a>",
                               extra_tags='safe')
                set = Event.objects.filter(date_start__gte=timezone.now()).order_by('date_start')
        else:
            set = Event.objects.filter(date_start__gte=timezone.now()).order_by('date_start')
    else:
        set = Event.objects.filter(date_start__gte=timezone.now()).order_by('date_start')

    for k in request.GET:
        if k == 'range':
            pass
        else:
            v = request.GET.get(k)
            if 'organization_id' in k:
                filters["Organization: " + str(Organization.objects.get(pk=v).name)] = k + '=' + v
            elif 'organization__name' in k:
                filters["Organization contains: " + v] = k + '=' + v
            elif 'name' in k:
                filters["Name contains: " + v] = k + '=' + v
            elif 'date' in k:
                raw_date = v.split('/')
                try:
                    v = datetime(int(raw_date[2]), int(raw_date[0]), int(raw_date[1]))
                    if k == 'date_start__gte':
                        filters["Date after: " + v] = k + '=' + v
                    elif k == 'date_start__lte':
                        filters["Date before: " + v] = k + '=' + v
                except:
                    messages.error(request, 'Invalid date!')
                    continue
            filter_dict[k] = v
        set = set.filter(**filter_dict)

    paginator = Paginator(set, 10, allow_empty_first_page=True)
    try:
        page_set = paginator.page(page)
    except PageNotAnInteger:
        page_set = paginator.page(1)
    except EmptyPage:
        messages.error(request, "That page was not found!")
        return HttpResponseRedirect('/')
    if not page_set.object_list.exists():
        messages.error(request, "No events found!")
    return render(request, 'main/list_events.html', {'events': page_set, 'filters': filters})

class EventView(generic.DetailView):
    model = Event
    template = 'main/event_detail.html'

def organization_detail(request, pk):
    o = get_object_or_404(Organization.objects, pk=pk)
    recent_events = list(o.events.filter(date_start__gte=timezone.now()).order_by('date_start')[:5])
    return render(request, 'main/org_detail.html', {'organization': o, 'recent_events': recent_events})

@login_required
def userevent_detail(request, pk):
    e = get_object_or_404(UserEvent.objects, pk=pk)
    if request.user.id == e.user_id or request.user.has_perm('auth.can_view'):
        return render(request, 'main/userevent_detail.html', {'userevent': e})
    messages.error(request, "That's not your event!")
    return HttpResponseRedirect('/')

@login_required
def userevent_edit(request, pk):
    e = get_object_or_404(UserEvent.objects, pk=pk)
    if request.user.id == e.user_id:
        if request.method == "GET":
            form = UserEventCreate(data=e.__dict__, user=request.user)
            return render(request, 'main/event_edit.html', {'event': form, 'userevent': True})
        form = UserEventCreate(data=request.POST, user=request.user, instance=e)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully')
            return HttpResponseRedirect(reverse('main:userevent_detail', args=(str(e.id),)))
        return render(request, 'main/event_edit.html', {'event': form, 'errors': form.errors, 'userevent': True})
    messages.error(request, "You aren't authorized to do that!")
    return HttpResponseRedirect(reverse('main:track'))

def userevent_verify(request, pk):
    e = get_object_or_404(UserEvent.objects, pk=pk)
    if request.method == "GET" and request.GET.get('key', 'abc') == e.email_verification_key:
        return render(request, 'main/userevent_verify.html', {'event': e, 'key': request.GET.get('key'), 'name': e.user.get_full_name()})
    elif request.method == "POST" and request.POST.get('key', 'abc') == e.email_verification_key:
        form = UserEventVerify(data=request.POST, instance=e)
        if form.is_valid():
            form.save(commit=False)
            e.advisor_approved = True
            e.save()
            messages.success(request, "Thank you for verifying {}'s NHS hours!".format(e.user.get_full_name()))
            return HttpResponseRedirect('/')
        return render(request, 'main/userevent_verify.html', {'event': form, 'key': request.GET.get('key'), 'error_message': form.errors, 'name': e.user.get_full_name()})
    return HttpResponseRedirect('/forbidden')

@login_required
def delete_userevent(request, pk):
    event = UserEvent.objects.get(pk=pk)
    if event:
        if request.user.id == event.user_id:
            event.delete()
            messages.info(request, "Event successfully deleted")
        else:
            messages.error(request, "You aren't authorized to do that!")
    else:
        messages.error(request, "Event not found!")
    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET.get('next'))
    return HttpResponseRedirect('/')

@login_required
def track_events(request):
    event = list(request.user.events.all())
    user_event = list(request.user.user_events.all())
    event_set = sorted(chain(event, user_event),
                       key=attrgetter('date_end'))
    total_hours = 0
    for i in event_set:
        total_hours += i.hours()

    if request.method == "POST":
        form = UserEventCreate(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully')
            return HttpResponseRedirect(reverse('main:track'))
        else:
            messages.error(request, 'Error creating event')
    else:
        form = UserEventCreate()
    return render(request, 'main/track_events.html', {'events': event_set,
                                                      'total_hours': total_hours,
                                                      'form': form})

def forbidden(request):
    """easy way to say that the user is not authorized"""
    messages.error(request, 'You aren\'t authorized to do that!')
    return HttpResponseRedirect('/')
