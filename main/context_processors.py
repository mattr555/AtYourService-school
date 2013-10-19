from django.conf import settings

def school_name(request):
	name_extras = {}
	name_extras['SCHOOL_NAME'] = settings.SCHOOL_NAME
	name_extras['SCHOOL_NAME_SHORT'] = settings.SCHOOL_NAME_SHORT
	return name_extras
