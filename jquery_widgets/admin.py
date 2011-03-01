# -*- coding: utf-8 -*-

# Based on code from: Jannis Leidal, 2008 (http://jannisleidel.com/),
# Copyright (C) 2010: Sindre Røkenes Myren,

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

import operator
from django.db import models
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import admin
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

	Any field with a choices attribut can be listed as in 'jqw_radio_fields'
	with entires of type::

	 '<field_name>',

	Example
	-------
	::
	 jqw_radios_fields = (
	     'gender',
	 )
	"""

	LOOKUP_CHOICES = 1

	def formfield_for_dbfield(self, db_field, **kwargs):
		""" Overrides the default widget for Foreignkey fields if they are
		specified in the related_search_fields class attribute.

		"""
		if db_field.name in self.jqw_autocomplete_fields:
			lookup = self.jqw_autocomplete_fields[db_field.name]
			if lookup == self.LOOKUP_CHOICES:
				kwargs['widget'] = AutocompleteInput(
						choices=db_field.get_choices(include_blank=False)
				)
			elif isinstance(db_field, models.ForeignKey):
				kwargs['widget'] = ForeignKeyAutocompleteInput(
					rel=db_field.rel,
					lookup_fields=self.jqw_autocomplete_fields[db_field.name]
				)
			elif isinstance(db_field, models.ManyToManyField):
				# FIXME
				pass
		return admin.ModelAdmin.formfield_for_dbfield(self, db_field,
				**kwargs)


#### Classes kept for bacward compabillity only ###

class ExtendedModelAdmin(JQWAdminMixin, admin.ModelAdmin):

	def formfield_for_dbfield(self, db_field, **kwargs):
		# 'related_search_fields' has been deprecated in favour of
		# 'jqw_autocomplete_fields'.
		self.jqw_autocomplete_fields = self.related_search_fields
		return super(ExtendedModelAdmin, self).formfield_for_dbfield(db_field,
				**kwargs)

