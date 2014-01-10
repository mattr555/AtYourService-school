from social.pipeline.partial import partial
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from main.models import UserProfile

@partial
def add_userprof(strategy, details, user=None, is_new=False, *args, **kwargs):
	try:
		up = user.user_profile
		if strategy.session_get('saved_timezone'):
			up.timezone = strategy.session_pop('saved_timezone')
			up.grad_class = strategy.session_pop('saved_grad_class')
			up.membership_status = strategy.session_pop('saved_member_status')
			up.save()
		return
	except:
		UserProfile(user=user, email_valid=True, grad_class=2000, membership_status='MEM').save()
		return HttpResponseRedirect(reverse('main:social_user_new'))
	
