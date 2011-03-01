# -*- coding: utf-8 -*-

# Based on code from: Jannis Leidal's blog 2008 (http://jannisleidel.com/),
# Copyright (C) 2010: Sindre Røkenes Myren,

import operator

from django.db import models
from django.http import HttpResponse, HttpResponseNotFound
from django.utils.encoding import smart_str

def __construct_search(field_name):
	# use different lookup methods depending on the notation
	if field_name.startswith('^'):
		return "%s__istartswith" % field_name[1:]
	elif field_name.startswith('='):
		return "%s__iexact" % field_name[1:]
	elif field_name.startswith('@'):
		return "%s__search" % field_name[1:]
	else:
		return "%s__icontains" % field_name

def fk_autocomplete_lookup(request, q=None):
	"""Searches in the fields of the given related model and returns the
	result as a simple string to be used by the jQuery Autocomplete plugin

	"""
	query_string = request.GET.get('q', None)
	app_label = request.GET.get('app_label', None)
	model_name = request.GET.get('model_name', None)
	lookup_fields = request.GET.get('lookup_fields', None)
	if not lookup_fields and app_label and model_name and query_string:
		return HttpResponseNotFound()

	fields = lookup_fields.split(',')
	model = models.get_model(app_label, model_name)
	qs = model._default_manager.all()
	for word in query_string.split():
		or_queries = [models.Q(**{__construct_search(smart_str(f)):
				smart_str(word)}) for f in fields]
		other_qs = models.query.QuerySet(model)
		other_qs.dup_select_related(qs)
		other_qs = other_qs.filter(reduce(operator.or_, or_queries))
		qs = qs | other_qs
	data = u'{"objects":[%s]}' % ','.join(
		('{"label":"%s","val":%s}' % (unicode(m), m.pk) for m in qs)
	)
	response = HttpResponse(data)
	response['Content-Type'] = 'text/json; charset=utf-8'
	return response
