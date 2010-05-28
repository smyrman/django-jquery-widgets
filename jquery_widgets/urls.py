# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
	url(r'^fk-search/$', 'jquery_widgets.views.fk_search',
		name="fk-search"),
	url(r'^fk-search/(.*)$', 'jquery_widgets.views.fk_search',
		name="fk-search-q"),
)
