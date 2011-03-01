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

from jquery_widgets.widgets import ForeignKeySearchInput

class ModelAdminMixin(object):
	"""Enables you to configure jQury UI widgets in the admin.

	# autocomplete_fields #
	For fields of type 'ForeignKey' and 'ManyToMany', you can configure the
	'autocomplete_fields' with entries of type:
	'<field_name>' : ('<lookup_field1>', '<lookup_field>')
	or:
	'<field_name>' : self.LOOKUP_AUTO

	For any other field type where you have configured 'choices', you may add
	entires of the latest type only.

	## Example ##
	autocomplete_fields = {
		'user': ('username', 'email'),
		'gender': self.LOOKUP_AUTO,
	}

	"""

	LOOKUP_AUTO =

	def formfield_for_dbfield(self, db_field, **kwargs):
		""" Overrides the default widget for Foreignkey fields if they are
		specified in the related_search_fields class attribute.

		"""
		if isinstance(db_field, models.ForeignKey) and \
				db_field.name in self.related_search_fields:
			kwargs['widget'] = ForeignKeySearchInput(db_field.rel,
									self.related_search_fields[db_field.name])
		return super(ExtendedModelAdmin, self).formfield_for_dbfield(db_field,
				**kwargs)


#### Classes kept for bacward compabillity only ###

class ExtendedModelAdmin(admin.ModelAdmin, ModelAdminMixin):
	pass

