from django.test import TestCase
from django.utils import timezone

from main.models import User, UserProfile, Organization, Event, UserEvent, Group, Demerit, haversin
import string
import random
import pytz
from collections import namedtuple

def create_test_user(name=None):
    if not name: # pragma: no cover
        name = ''.join([random.choice(string.ascii_letters) for i in range(10)])
    user = User.objects.create_user(name, 'test@mailinator.com', name)
    prof = UserProfile(user=user, timezone='America/New_York', email_valid=True, grad_class=2016, 
        membership_status='CAN', location='New York City, NY')
    prof.save()
    return user

def create_test_organization(u=None):
    if not u: # pragma: no cover
        u = create_test_user()
    o = Organization(name='org', description='we do stuff', location='New York City, NY', admin=u)
    o.save()
    return o

def create_test_event(u=None, o=None):
    if not o: # pragma: no cover
        o = create_test_organization(u)
    e = Event(name='do stuff', organizer=o.admin, organization=o, description='yeah', date_start=timezone.now(),
        date_end=timezone.now() + timezone.timedelta(hours=1), location='New York City, NY', hour_type='SRV')
    e.save()
    return e

def create_test_userevent(u=None):
    if not u: # pragma: no cover
        u = create_test_user()
    e = UserEvent(name='do stuff', user=u, organization='do stuff org', description='yeah', date_start=timezone.now(), 
        date_end=timezone.now() + timezone.timedelta(hours=1), location='New York City, NY', hour_type='SRV', hours_worked=1)
    e.save()
    return e

class EventTest(TestCase):
    def setUp(self):
        self.organizer = create_test_user('organizer')
        self.e = create_test_event(self.organizer, None)

    def test_event_str(self):
        self.assertEqual(str(self.e), 'do stuff')

    def test_event_hours(self):
        self.assertEqual(self.e.hours(), 1)
        self.e.nhs_approved = False
        self.assertEqual(self.e.hours(), 0)

    def test_event_detail_url(self):
        self.assertIn('event', self.e.detail_url())
        self.assertIn(str(self.e.pk), self.e.detail_url())

    def test_event_status(self):
        self.assertEqual(self.e.status(self.organizer), 'Organizing')
        self.assertEqual(self.e.row_class(self.organizer), '')
        self.e.nhs_approved = False
        self.assertEqual(self.e.status(self.organizer), 'Not approved by NHS')
        self.assertEqual(self.e.row_class(self.organizer), 'danger')
        self.e.nhs_approved = True
        new_user = create_test_user('test2')
        self.assertEqual(self.e.status(new_user), 'Not participating')
        self.assertEqual(self.e.row_class(new_user), '')
        self.e.participants.add(new_user)
        self.assertEqual(self.e.status(new_user), 'Unconfirmed')
        self.assertEqual(self.e.row_class(new_user), 'warning')
        self.assertEqual(self.e.confirm_status(new_user).button_class, 'btn-success')
        self.assertEqual(self.e.confirm_status(new_user).button_text, 'Confirm')
        self.e.confirmed_participants.add(new_user)
        self.assertEqual(self.e.status(new_user), 'Confirmed')
        self.assertEqual(self.e.row_class(new_user), 'success')
        self.assertEqual(self.e.confirm_status(new_user).button_class, 'btn-warning')
        self.assertEqual(self.e.confirm_status(new_user).button_text, 'Unconfirm')
        self.e.date_start += timezone.timedelta(days=5)
        self.assertEqual(self.e.status(new_user), 'Event has not occurred yet')
        self.assertEqual(self.e.row_class(new_user), '')
        self.e.participants.clear()
        self.e.confirmed_participants.clear()
        self.e.date_start = timezone.make_aware(timezone.datetime(timezone.now().year, timezone.now().month, 1) 
            - timezone.timedelta(hours=1), timezone.utc)
        self.assertIn('last-month', self.e.row_class(new_user))

    def test_event_getOrganization(self):
        self.assertEqual(self.e.getOrganization(), 'org')

    def test_event_participant_count(self):
        self.assertEqual(self.e.participant_count(), 0)
        new_user = create_test_user()
        self.e.participants.add(new_user)
        self.assertEqual(self.e.participant_count(), 1)
        self.e.participants.clear()

    def test_event_date_input(self):
        self.assertRegex(self.e.date_start_input(), '(\d{2}/){2}\d{2} \d{2}:\d{2} (AM|PM)')
        self.assertRegex(self.e.date_end_input(), '(\d{2}/){2}\d{2} \d{2}:\d{2} (AM|PM)')

    def test_event_populate_geo(self):
        self.e.populate_geo()
        self.assertEqual(round(self.e.geo_lat,4), 40.7144)
        self.assertEqual(round(self.e.geo_lon,4), -74.006)

    def test_haversin(self):
        self.assertEqual(int(haversin(40.7144, -74.006, 34.406, -118.612)), 2455)

    def test_event_within(self):
        loc = namedtuple('LocTuple', 'geo_lat geo_lon')
        point = loc(40.166, -74.082)
        self.e.populate_geo()
        self.e.save()
        self.assertTrue(self.e not in Event.objects.within(point, 20))
        self.assertTrue(self.e in Event.objects.within(point, 100))

class UserEventTest(TestCase):
    def setUp(self):
        self.user = create_test_user('ue_test')
        self.e = create_test_userevent(self.user)

    def test_userevent_str(self):
        self.assertEqual(str(self.e), 'do stuff')

    def test_userevent_hours(self):
        self.assertEqual(self.e.hours(), 1)
        self.e.nhs_approved = False
        self.assertEqual(self.e.hours(), 0)

    def test_userevent_detail_url(self):
        self.assertIn('event', self.e.detail_url())
        self.assertIn(str(self.e.pk), self.e.detail_url())

    def test_userevent_status(self):
        self.assertEqual(self.e.status(self.user), 'User-created Event')
        self.assertEqual(self.e.row_class(self.user), 'success')
        self.e.nhs_approved = False
        self.assertEqual(self.e.status(self.user), 'Not approved by NHS')
        self.assertEqual(self.e.row_class(self.user), 'danger')
        self.e.nhs_approved = True
        new_user = create_test_user('test3')
        self.assertEqual(self.e.status(new_user), 'Not participating')
        self.assertEqual(self.e.row_class(new_user), '')
        self.e.date_start += timezone.timedelta(days=5)
        self.assertEqual(self.e.status(self.user), 'Event has not occurred yet')
        self.assertEqual(self.e.row_class(self.user), '')
        self.e.date_start = timezone.make_aware(timezone.datetime(timezone.now().year, timezone.now().month, 1) 
            - timezone.timedelta(hours=1), timezone.utc)
        self.assertIn('last-month', self.e.row_class(self.user))

    def test_userevent_getOrganization(self):
        self.assertEqual(self.e.getOrganization(), 'do stuff org')

    def test_userevent_populate_geo(self):
        self.e.populate_geo()
        self.assertEqual(round(self.e.geo_lat,4), 40.7144)
        self.assertEqual(round(self.e.geo_lon,4), -74.006)

class OrganizationTest(TestCase):
    def setUp(self):
        self.o = create_test_organization()

    def test_org_str(self):
        self.assertEqual(str(self.o), 'org')

    def test_org_detail_url(self):
        self.assertIn('organization', self.o.detail_url())
        self.assertIn(str(self.o.pk), self.o.detail_url())

    def test_org_member_count(self):
        self.assertEqual(self.o.member_count(), 0)
        new_user = create_test_user('test4')
        self.o.members.add(new_user)
        self.assertEqual(self.o.member_count(), 1)

    def test_org_event_count(self):
        self.assertEqual(self.o.event_count(), 0)
        create_test_event(None, self.o)
        self.assertEqual(self.o.event_count(), 1)

    def test_org_populate_geo(self):
        self.o.populate_geo()
        self.assertEqual(round(self.o.geo_lat,4), 40.7144)
        self.assertEqual(round(self.o.geo_lon,4), -74.006)

class UserProfileTest(TestCase):
    def setUp(self):
        self.u = create_test_user('up_test')
        self.u.first_name = 'Joe'
        self.u.last_name = 'Momma'
        self.up = self.u.user_profile

    def test_userprof_str(self):
        self.assertEqual(str(self.up), 'Joe Momma')

    #would like to test True case, but _group_perm_cache seems to be a limitation..
    def test_userprof_nhsadmin(self):
        self.assertFalse(self.up.is_nhs_admin())

    def test_userprof_orgadmin(self):
        self.assertFalse(self.up.is_org_admin())

    def test_userprof_volunteer(self):
        self.assertFalse(self.up.is_volunteer())

    def test_userprof_service_hours(self):
        self.assertEqual(self.up.service_hours(), 0)
        e = create_test_event()
        e.participants.add(self.u)
        self.assertEqual(self.up.service_hours(), 1)
        e.participants.clear()

    def test_userprof_leadership_hours(self):
        self.assertEqual(self.up.leadership_hours(), 0)
        UserEvent(name='do stuff', user=self.u, organization='do stuff org', description='yeah', date_start=timezone.now(), 
            date_end=timezone.now() + timezone.timedelta(hours=1), location='New York City, NY', hour_type='LED', 
            hours_worked=1).save()
        self.assertEqual(self.up.leadership_hours(), 1)

    def test_userprof_service_hours_last_month(self):
        self.assertEqual(self.up.service_hours_last_month(), 0)
        e = create_test_event()
        e.participants.add(self.u)
        e.date_start = timezone.make_aware(timezone.datetime(timezone.now().year, timezone.now().month, 1) 
            - timezone.timedelta(hours=1), pytz.timezone('America/New_York'))
        e.date_end = e.date_start + timezone.timedelta(hours=1)
        e.save()
        self.assertEqual(self.up.service_hours_last_month(), 1)

    def test_userprof_populate_geo(self):
        self.up.populate_geo()
        self.assertEqual(round(self.up.geo_lat,4), 40.7144)
        self.assertEqual(round(self.up.geo_lon,4), -74.006)

    def test_userprof_demerit_count(self):
        self.assertEqual(self.up.demerit_count(), 0)
        Demerit(user=self.u, reason='just because').save()
        self.assertEqual(self.up.demerit_count(), 1)
