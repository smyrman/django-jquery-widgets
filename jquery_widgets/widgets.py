# -*- coding: utf-8 -*-

# Based on code from Jannis Leidel's blog 2008 (http://jannisleidel.com/)
# Copyright (C) 2010: Sindre Røkenes Myren,

from django import VERSION, forms
from django.conf import settings
from django.utils.safestring import mark_safe, mark_for_escaping as esc
from django.utils.text import truncate_words
from django.template.loader import render_to_string
from django.conf import settings

__all__ = ("AutocompleteInput", "ForeignKeyAutocompleteInput",
"ManyToManyAutocompleteInput")

class AutocompleteInput(forms.HiddenInput):
	"""Replaces the default 'select' box with a autocomplete drop-down for any
	widget with a choies attribute.

	"""
	TEMPLATE = 'jquery_widgets/autocomplete_input.html'

	class Media:
		css = {"all": [
				settings.STATIC_URL+"css/jquery-ui-themes/{{theme}}/style.css",
			],
		}
		js = (
			settings.ADMIN_MEDIA_PREFIX+"js/jquery.min.js",
			settings.ADMIN_MEDIA_PREFIX+"js/jquery.init.js",
			settings.STATIC_URL+"js/django.jquery.reinit.js",
			settings.STATIC_URL+"js/jquery-ui.min.js",
		)
	def __init__(self, attrs=None, choices=(), theme=None,
			use_admin_icons=True):
		self.choices = choices
		#self.theme = theme or settings.JQUERY_UI_THEME
		self.theme = 'ui-admin'
		self.use_admin_icons = use_admin_icons
		self.Media.css['all'][0] =\
				self.Media.css['all'][0].replace('{{theme}}', self.theme)
		super(AutocompleteInput, self).__init__(attrs)

	def label_for_value(self, value):
		for v, label in self.choices:
			if value == v:
				return label
		return value

	def render(self, name, value, attrs={}):
		rendered = super(AutocompleteInput, self).render(name, value, attrs)
		if value != None:
			value_label = self.label_for_value(value)
		else:
			value_label = u''
		if len(self.choices) > 0:
			source = mark_safe(u'[%s]' %
					u','.join((u'{"val":"%s","label":"%s"}' %
					(esc(i[0]), esc(i[1])) for i in self.choices)))
		else:
			source = u''

		d = {
			'rendered': rendered,
			'name': name,
			'value': value_label,
			'source': source,
			'use_admin_icons': self.use_admin_icons,
			'admin_media_prefix': settings.ADMIN_MEDIA_PREFIX,
		}
		return render_to_string(self.TEMPLATE, d)


class ForeignKeyAutocompleteInput(AutocompleteInput):
	""" A Widget for displaying ForeignKeys in an autocomplete search input
	instead in a ``select`` box.
	"""

	TEMPLATE = 'jquery_widgets/fk_autocomplete_input.html'

	def __init__(self, attrs=None, rel=None, lookup_fields=None, **kwargs):
		self.rel = rel
		self.lookup_fields = lookup_fields
		super(ForeignKeyAutocompleteInput, self).__init__(attrs, **kwargs)

	def label_for_value(self, value):
		key = self.rel.get_related_field().name
		obj = self.rel.to._default_manager.get(**{key: value})
		return truncate_words(obj, 14)

	def render(self, name, value, attrs={}):
		rendered = super(AutocompleteInput, self).render(name, value, attrs)
		if value:
			value_label = self.label_for_value(value)
		else:
			value_label = u''

		d = {
			'rendered': rendered,
			'name': name,
			'value': value_label,
			'lookup_fields': ','.join(self.lookup_fields),
			'model_name': self.rel.to._meta.module_name,
			'app_label': self.rel.to._meta.app_label,
			'use_admin_icons': self.use_admin_icons,
			'admin_media_prefix': settings.ADMIN_MEDIA_PREFIX,
		}
		return render_to_string(self.TEMPLATE, d)


class ManyToManyAutocompleteInput(ForeignKeyAutocompleteInput):
	""" A Widget for displaying ForeignKeys in an autocomplete search input
	instead in a ``select`` box.
	"""
	TEMPLATE = 'jquery_widgets/mm_autocomplete_input.html'
