AtYourService-School
====================

[![Build Status](https://travis-ci.org/mattr555/AtYourService-school.png?branch=develop)](https://travis-ci.org/mattr555/AtYourService-school)
[![Coverage Status](https://coveralls.io/repos/mattr555/AtYourService-school/badge.png?branch=develop)](https://coveralls.io/r/mattr555/AtYourService-school?branch=develop)

A django-based app to track your service hours on the web

This is the version of AtYourService to run on a school domain

For the future standalone website, go [here](https://www.github.com/AtYourService)

[Vision doc here](TODO.txt)

Withheld settings files
=======================
dev_settings.py/prod_settings.py
--------------------------------

* `DATABASES`
* `STATIC_ROOT`
* `STATICFILES_DIRS`
* `TEMPLATE_DIRS`
* `EMAIL_BACKEND`
* `DEFAULT_FROM_EMAIL`
* `LOGGING`
* `CACHES`
* `ALLOWED_HOSTS`

personal_settings.py
--------------------

* `SECRET_KEY`
* `ADMINS`
* `MANAGERS`
* `SCHOOL_NAME`
* `SCHOOL_NAME_SHORT`

Changelog
=========

v0.1.0
------
Initial release. Corresponds with AtYourService v0.1.0

* +User account manipula tion
* +Email notification
* +Organization manipulation and administration
* +Confirmation of user attendance
* +Email verification

v0.2.0
------

* +NHS Admin page:
	* view reports of students
	* disapprove of bad events
	* demerits
* +Travis CI/Coveralls
* +Member vs. Candidate rules and tracking
* +Monthly rules for members

v0.3.0
------

* +Login with Google
