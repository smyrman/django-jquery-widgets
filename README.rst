This project is no longer maintained.


=====================
Django jQuery Widgets
=====================

This is a pluggable app for Django based on jQuery UI. The goal of this project
is to make available a subset of jQuery UI's widgets for django programmers,
using a decent level of abstraction.

This is the documentation for the development version. There are significant
changes between this version and the latest release.

Application content
===================

Included widgets
----------------

*JQWAutocompleteSelect*: A jQuery UI replacement for the html 4 select box
input.

*JQWAutocompleteFKSelect*: A variant of the above widget for ForeignKeys
only. It uses ajax to lookup choices in your database, based on *lookup
fields* that you provide.

Unfinished widgets
------------------
*If you want to help finish these, make a fork!*

*JQWRadioSelect*: This one uses jQuery UI buttons instead of normal radio
buttons. Note that the current implementation is kind of buggy, and it does not
work well in the django admin.

*JQWCheckboxSelect*: Same as above, but for chekboxes - probably not hard to
implement once *JQWRadioSelect* is complete.

*JQWAutocompleteSelectMultiple*: Not finished.

*JQWAutocompleteM2MSelecMultiple*: A version of the above widget, but for
ManyToMany fields only, and with dynamic ajax searching.


Included for the admin
----------------------

*JQWAdminMixin*: A mixin for django.admin's ModelAdmin and InlineAdmin
classes that make it easy to use the included widgets in the admin view.

Example usage::

 from django.contrib import admin

 from jquery_widgets.admin import JQWAdminMixin
 from myapp.models import MyModel

 class MyModelAdmin(JQWAdminMixin, admin.ModelAdmin):
      ...
      # Use the JQWAutocompleteFKSelect widget for the ForeignKey field #
      # 'user'. Let the lookup_fields be 'username' and 'email'. Use the
      # JQWAutocompleteSelect widget for the IntegerField 'type'.
      jqw_autocomplete_fields = {
        'user': ('username', 'email'),
        'type': JQWAdminMixin.LOOKUP_CHOICES
      }

A more detailed description with examples is available in the JQWAdminMixin's
doc string.

**NB!** Make sure that you always place *JQWAdminMixin* **before**
*admin.ModelAdmin*! If you don't do this, Python will use admin.ModelAdmin's
*formfield_for_dbfield()* method, and nothing will work for you!


*ExtendedModelAdmin*: This class is deprecated in favour of *JQWAdminMixin*,
but is kept for bacward compability. It allows you to use
*foreign_key_search_fields* instead of *jqw_autocomplete_fields*.

Installation
============

Using pip (or easy_install):
----------------------------

Stable::

  $ sudo pip install django-jquery-widgets

Development::

  $ sudo pip install -e git://github.com/smyrman/django-jquery-widgets.git#egg=django-jquery-widgets


Using git:
----------

If you want to include the code with your django project, rather then
installing it to your system, you can download a recent version and copy the
jquery_widgets folder into your django project.

Git::

  $ git clone git://github.com/smyrman/django-jquery-widgets.git

Project configuration
=====================

Quick guide
-----------

1. Add 'jquery_widgets' to your settings.INSTALLED_APPS

2. Add This line to your urlconf::

    url(r'^jqw/', include('jquery_widgets.urls', namespace='jquery-widgets')),

   Note that you are free to call the url something else then 'jqw'. The urls are
   not hardcoded in jquery_widgets!

3. The current development version workes well with Django 1.3's staticfiles
   app. That means you can symlink or copy the static media into your
   STATIC_ROOT (needed for production only), by issuing::

    $ python manage.py -l collectstatic

   Note that you need to have 'django.contrib.staticfiles' in your INSTALLED_APPS
   for the above command to work. If you want to use this version of
   django-jquery-widgets with an older version of Django then 1.3, you have to
   manually copy the files from 'jqury_widgets/static' into your MEDIA_ROOT
   folder.

Planned configuration parameters (not jet implemented)
------------------------------------------------------

Planned defaults::

 # New themes can be added as:
 # <STATIC_ROOT>/css/jquery-ui-themes/<theme name>/style.css

 JQUERY_UI_THEME = {
         'admin': 'ui-admin',       # Theme to use in django admin.
         'default': 'ui-lightness', # Default theme for widgets.
 }

