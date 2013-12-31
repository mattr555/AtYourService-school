from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group
from django.contrib.sites.models import Site
from south.signals import post_migrate
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist

from main.models import SiteSettings, UserProfile, User

# custom user related permissions
def add_user_permissions(sender, **kwargs):
    pass

def add_groups(sender, **kwargs):
    ct = ContentType.objects.get(app_label='auth', model='user')
    perm, created = Permission.objects.get_or_create(codename='can_view', name='Can View Users', content_type=ct)

    group, created = Group.objects.get_or_create(name='Volunteer')
    if created:
        p = Permission.objects.get(codename='add_userevent')
        group.permissions.add(p)
    group, created = Group.objects.get_or_create(name='Org_Admin')
    if created:
        p = Permission.objects.get(codename='add_organization')
        group.permissions.add(p)
    group, created = Group.objects.get_or_create(name='NHS_Admin')
    if created:
        p = Permission.objects.get(codename='can_view')
        group.permissions.add(p)
    if not SiteSettings.objects.exists():
        settings = SiteSettings(site=Site.objects.get(pk=1), candidate_leadership_hours=50, 
            candidate_service_hours=100, member_service_hours=6).save()

def create_userprof(sender, instance, created, **kwargs):
    """for when the user is created on the first syncdb"""
    if created and instance.is_superuser:
        try:
            up = instance.user_profile
        except ObjectDoesNotExist:
            UserProfile(user=instance, email_valid=True, grad_class=2000, membership_status='MEM').save()

#post_migrate.connect(add_user_permissions, sender=auth_models)
post_migrate.connect(add_groups)
post_save.connect(create_userprof, sender=User, dispatch_uid="create_userprof")

