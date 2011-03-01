# -*- coding: utf-8 -*-

# Based on code from: Jannis Leidal, 2008 (http://jannisleidel.com/),
# Copyright (C) 2010: Sindre Røkenes Myren,

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

import operator
from django.db import models
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin
from django.utils.encoding import smart_str

from jquery_widgets.widgets import *

__all__ = ('JQWAdminMixin', 'ExtendedModelAdmin')

class JQWAdminMixin(object):
	"""Enables you to configure jQury UI widgets in the admin.

	jqw_autocomplete_fields
	=======================

	For fields of type 'ForeignKey' and 'ManyToMany', you can configure the
	'jqw_autocomplete_fields' with entries of type::

	'<field_name>' : ('<lookup_field1>', '<lookup_field2>'),
	or::

	'<field_name>' : JQWAdminMixin.LOOKUP_CHOICES,

	For any other field type where you have configured 'choices', you may add
	entires of the latest type only.

	Example
	-------
	::
	 jqw_autocomplete_fields = {
	     'user': ('username', 'email'),
	     'group': JQWAdminMixin.LOOKUP_CHOICES,
	 }

	jqw_radio_fields
	================

	WARNING: Currently works kind of crap in good in the admin!
	Any field with a choices attribut can be listed as in 'jqw_radio_fields'
	with entires of type::

	 '<field_name>': <allignment>,

	Note that this syntax is identical to the the existing ModelAdmin's
	'radio_fields'. Also note that currently, the <allignment> parameter is
	ignored.

	Example
	-------
	::
	 jqw_radio_fields = {
		 'gender': JQWAdminMixin.HORIZONTAL
	 }
	"""

	LOOKUP_CHOICES = 1
	HORIZONTAL = admin.HORIZONTAL
	VERTICAL = admin.VERTICAL

	def formfield_for_dbfield(self, db_field, **kwargs):
		if db_field.name in self.jqw_autocomplete_fields:
			lookup = self.jqw_autocomplete_fields[db_field.name]
			if lookup == self.LOOKUP_CHOICES:
				kwargs['widget'] = JQWAutocompleteSelect(
					choices=db_field.get_choices(include_blank=False),
					theme='ui-admin',
					#theme=settings.JQUERY_UI_THEME['admin'],
					use_admin_icons=True,
				)
			elif isinstance(db_field, models.ForeignKey):
				kwargs['widget'] = JQWAutocompleteFKSelect(
					rel=db_field.rel,
					lookup_fields=self.jqw_autocomplete_fields[db_field.name],
					theme='ui-admin',
					#theme=settings.JQUERY_UI_THEME['admin'],
					use_admin_icons=True,
				)
			elif isinstance(db_field, models.ManyToManyField):
				# FIXME
				pass
		elif db_field.name in self.jqw_radio_fields:
			align = self.jqw_radio_fields[db_field.name]
			kwargs['widget'] = JQWRadioSelect(
					theme='ui-admin',
					#theme=settings.JQUERY_UI_THEME['admin'],
					)
		return BaseModelAdmin.formfield_for_dbfield(self, db_field, **kwargs)


#### Classes kept for bacward compabillity only ###

class ExtendedModelAdmin(JQWAdminMixin, admin.ModelAdmin):

	def formfield_for_dbfield(self, db_field, **kwargs):
		# 'related_search_fields' has been deprecated in favour of
		# 'jqw_autocomplete_fields'.
		if hasattr(self, "related_search_fields"):
			self.jqw_autocomplete_fields = self.related_search_fields

		return super(ExtendedModelAdmin, self).formfield_for_dbfield(db_field,
				**kwargs)

