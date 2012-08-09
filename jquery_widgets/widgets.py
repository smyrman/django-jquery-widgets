# -*- coding: utf-8 -*-

# Based on code from Jannis Leidel's blog 2008 (http://jannisleidel.com/)
# Copyright (C) 2010: Sindre Røkenes Myren,

from django import forms
from django.forms.util import flatatt
from django.forms.widgets import RadioFieldRenderer, Widget
from django.utils.safestring import mark_safe, mark_for_escaping as esc
from django.utils.text import truncate_words
from django.template.loader import render_to_string
from django.conf import settings

__all__ = (
	"JQWWidgetMixin", "JQWSelectMixin", "JQWAutocompleteSelect",
	"JQWAutocompleteFKSelect", "JQWAutocompleteSelectMultiple",
	"JQWAutocompleteM2MSelectMultiple", "JQWRadioSelect", "JQWCheckboxSelect",
)

try:
	ADMIN_MEDIA_PREFIX = settings.ADMIN_MEDIA_PREFIX
except AttributeError:
	ADMIN_MEDIA_PREFIX = '%sadmin/' % settings.STATIC_URL

class JQWWidgetMixin(object):
	"""Base mixin class for all jQuory UI based widgets.

	"""
	CSS_PATH = "css/jquery-ui-themes/{{theme}}/style.css"
	jqw_input_type = 'text'

	class Media:
		css = {"all": ['THEME GOES HERE'],}
		js = (
			ADMIN_MEDIA_PREFIX+"js/jquery.min.js",
			ADMIN_MEDIA_PREFIX+"js/jquery.init.js",
			settings.STATIC_URL+"js/django.jquery.reinit.js",
			settings.STATIC_URL+"js/jquery-ui.min.js",
		)

	def set_theme(self, theme):
		if theme == None:
			#theme = theme or settings.JQUERY_UI_THEME['default']
			theme = 'ui-admin'
		self.Media.css['all'][0] = settings.STATIC_URL +\
				self.CSS_PATH.replace('{{theme}}', theme)

	def _render_parrent(self, name, value, attrs, **kwargs):
		raise NotImplemented

	def _get_jqw_value(self, value):
		return ''

	def build_attrs(self, extra_attrs={}, name='', **kwargs):
		name = extra_attrs.get('name', name)
		extra_attrs['id'] = extra_attrs.get('id', 'id_'+name)
		return Widget.build_attrs(self, extra_attrs, **kwargs)

	def build_jqw_attrs(self, extra_attrs=None, value=None, **kwargs):
		final_attrs = self.build_attrs(extra_attrs, **kwargs)
		final_attrs['id'] += '_jqw'
		final_attrs['type'] = self.jqw_input_type
		jqw_value = self._get_jqw_value(value)
		if jqw_value != '' and self.jqw_input_type == 'text':
			final_attrs['value'] = esc(jqw_value)
		return final_attrs

	def _build_base_dict(self, name, value, attrs, **kwargs):
		final_attrs = self.build_attrs(attrs, name=name)
		rendered = self._render_parrent(name, value, attrs=final_attrs,
				**kwargs)
		id = final_attrs['id']
		final_attrs = self.build_jqw_attrs(final_attrs, value=value)
		d = {
			'rendered': rendered,
			'attrs': mark_safe(flatatt(final_attrs)),
			'value': attrs.get('value', ''),
			'id': id,
		}
		return d


class JQWSelectMixin(JQWWidgetMixin):
	""" Base mixin class for all select like jQuoery UI widgets.

	"""
	def _get_jqw_value(self, value):
		# GUARD: No value?
		if value in (None, u''):
			return ''

		label = unicode(value)
		for v, l in self.choices:
			if value == v:
				label = l
		return truncate_words(label, 14)


### jQuery UI Autocomplete widgets ###

class JQWAutocompleteSelect(JQWSelectMixin, forms.HiddenInput):
	"""Replaces the default 'select' box with a autocomplete drop-down for any
	widget with a choies attribute.

	"""
	template = 'jquery_widgets/autocomplete_select.html'
	jqw_input_type = 'text'

	def __init__(self, attrs=None, choices=(), theme=None,
			use_admin_icons=False, min_length=0):
		self.set_theme(theme)
		self.choices = choices
		self.use_admin_icons = use_admin_icons
		self.min_length = min_length
		super(JQWAutocompleteSelect, self).__init__(attrs)

	def _render_parrent(self, name, value, attrs, **kwargs):
		return super(JQWAutocompleteSelect, self).render(name, value, attrs,
				**kwargs)

	def _build_base_dict(self, name, value, attrs):
		d = super(JQWAutocompleteSelect, self)._build_base_dict(name, value,
				attrs)
		d['min_length'] = self.min_length
		d['use_admin_icons'] = self.use_admin_icons
		d['admin_media_prefix'] = settings.ADMIN_MEDIA_PREFIX
		return d

	def render(self, name, value, attrs=None, choices=()):
		d  = self._build_base_dict(name, value, attrs)
		if len(choices) > 0:
			d['source'] = mark_safe(u'[%s]' %
					u','.join((u'{"val":"%s","label":"%s"}' %
					(esc(i[0]), esc(i[1])) for i in choices)))
		else:
			d['source'] = u'[]'
		return render_to_string(self.template, d)


class JQWAutocompleteFKSelect(JQWAutocompleteSelect):
	""" A Widget for displaying ForeignKeys in an autocomplete search input
	instead in a ``select`` box.
	"""

	template = 'jquery_widgets/autocomplete_fk_select.html'

	def __init__(self, attrs=None, choices=(), min_length=2, rel=None,
			lookup_fields=None, **kwargs):
		self.rel = rel
		self.lookup_fields = lookup_fields
		super(JQWAutocompleteFKSelect, self).__init__(attrs=attrs,
				min_length=min_length, **kwargs)

	def _get_jqw_value(self, value):
		# GUARD: No value?
		if value in (None, u''):
			return ''

		key = self.rel.get_related_field().name
		obj = self.rel.to._default_manager.get(**{key: value})
		return truncate_words(obj, 14)

	def render(self, name, value, attrs=None, choices=()):
		d = self._build_base_dict(name, value, attrs)
		d['lookup_fields'] = ','.join(self.lookup_fields)
		d['model_name'] = self.rel.to._meta.module_name
		d['app_label'] = self.rel.to._meta.app_label
		return render_to_string(self.template, d)


class JQWAutocompleteSelectMultiple(JQWAutocompleteSelect):
	template = 'jquery_widgets/autocomplete_select_multiple.html'
	#TODO: Implement!


class JQWAutocompleteM2MSelectMultiple(JQWAutocompleteFKSelect):
	template = 'jquery_widgets/autocomplete_m2m_select_multiple.html'
	#TODO: Implement!


### jQuery UI Buttton widgets ###

class JQWRadioFieldRenderer(RadioFieldRenderer):
	def render(self):
		id = self.attrs['id']
		self.attrs['name'] = id
		return mark_safe(u'<div id="%s">\n%s\n</div>' %
				(id, u'\n'.join([u'%s' % unicode(w) for w in self])))


class JQWRadioSelect(JQWSelectMixin, forms.RadioSelect):
	template = 'jquery_widgets/buttons_radio_select.html'
	renderer = JQWRadioFieldRenderer
	# FIXME: Works kind of crap! At least in the admin!

	def __init__(self, attrs=None, choices=(), theme=None, **kwargs):
		self.set_theme(theme)
		super(JQWRadioSelect, self).__init__(attrs, choices=choices, **kwargs)

	def _render_parrent(self, name, value, attrs, **kwargs):
		return super(JQWRadioSelect, self).render(name, value, attrs=attrs,
				**kwargs)

	def render(self, name, value, attrs=None, choices=()):
		d = self._build_base_dict(name, value, attrs, choices=choices)
		return render_to_string(self.template, d)


class JQWCheckboxSelect(JQWRadioSelect):
	template = 'jquery_widgets/buttons_checkbox_select.html'
	#TODO: Implement!


class JQWSlider(forms.widgets.TextInput):
	template = 'jquery_widgets/slider.html'
	
	def render(self, name, value, attrs=None):
		return render_to_string(self.template, {
			'min': self.min_value,
			'max': self.max_value,
			'step': self.step,
			'value': value or self.min_value,
			'name': name,
			'id': attrs['id']
		})