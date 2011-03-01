# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from views import fk_autocomplete_lookup

urlpatterns = patterns('',
	url(r'^fk-autocomplete/$', fk_autocomplete_lookup,
			name="fk-autocomplete"),
	url(r'^fk-autocomplete/(.*)$', fk_autocomplete_lookup,
			name="fk-autocomplete-q"),
)
