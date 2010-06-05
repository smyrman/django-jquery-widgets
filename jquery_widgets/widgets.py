# -*- coding: utf-8 -*-

# Based on code from Jannis Leidel's blog 2008 (http://jannisleidel.com/)
# Copyright (C) 2010: Sindre Røkenes Myren,

from django import VERSION, forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.text import truncate_words
from django.template.loader import render_to_string

# Get JQuery URL from settings, or fallback to default value:
JS_BASE = tuple() # Basic tuple of javascripts to extend.
try:
	JQUERY_URL = settings.JQUERY_URL
except AttributeError:
	JQUERY_URL = 'js/jquery.min.js'

	# Django 1.2 and later include a version of jQury in contrib.admin:
	if VERSION[:2] >= (1, 2):
		try:
			JQUERY_URL = settings.ADMIN_MEDIA_PREFIX + JQUERY_URL
			# Django admin keep it's jQuery in the 'django.jQuey' namespace,
			# which is kind of anoying. If we are to use jQury extensions
			# without modifications, we must make sure jQuery is put back into
			# the global namespace:
			JS_BASE = (
				settings.ADMIN_MEDIA_PREFIX+'jquery.init.js',
				'jquery_widgets/js/django.jquery.reinit.js',
			)
		except AttributeError:
			JQUERY_URL = 'js/jquery.min.js'

JS_BASE = (JQUERY_URL,) + JS_BASE



class ForeignKeySearchInput(forms.HiddenInput):
	""" A Widget for displaying ForeignKeys in an autocomplete search input
	instead in a ``select`` box.
	"""
	class Media:
		css = {
			'all': ('jquery_widgets/css/jquery.autocomplete.css',)
		}
		js = JS_BASE + (
			'jquery_widgets/js/jquery.autocomplete.min.js',
		)

	def label_for_value(self, value):
		key = self.rel.get_related_field().name
		obj = self.rel.to._default_manager.get(**{key: value})
		return truncate_words(obj, 14)

	def __init__(self, rel, search_fields, attrs=None):
		self.rel = rel
		self.search_fields = search_fields
		super(ForeignKeySearchInput, self).__init__(attrs)

	def render(self, name, value, attrs={}):
		rendered = super(ForeignKeySearchInput, self).render(name, value, attrs)
		if value:
			label = self.label_for_value(value)
		else:
			label = u''

		d = {
			'rendered': rendered,
			'current_app': 'jquery_widgets',
			'search_fields': ','.join(self.search_fields),
			'admin_media_prefix': settings.ADMIN_MEDIA_PREFIX,
			'model_name': self.rel.to._meta.module_name,
			'app_label': self.rel.to._meta.app_label,
			'label': label,
			'name': name,
		}
		return render_to_string('jquery_widgets/fk_search_input.html', d)
