# -*- coding: utf-8 -*-

# Based on code from Arne Brodowski's blog, http://www.arnebrodowski.de/blog/
# Copyright (C) 2010, Sindre Røkenes Myren.

import os
import sys
from django.conf import settings
from django.db.models import signals
from django.core.management.color import color_style

def link_app_media(sender, verbosity, **kwargs):
	"""Symlink 'media' folder for this app to settings.MEDIA_ROOT'/<app_name>'
	after syncdb has been run on a project that list this app in
	settings.INTALLED_APPS

	"""
	app_name = sender.__name__.split('.')[-2]
	# GUARD: In principal, this function can actually create a symling for
	# *all* apps containing a 'media' folder. But we will limit it to only
	# create symlinks for this particular app:
	if app_name != 'jquery_widgets':
		return

	app_dir = os.path.dirname(sender.__file__)

	app_media_dir = os.path.join(app_dir, 'media')

	if os.path.exists(app_media_dir):
		dest = os.path.join(settings.MEDIA_ROOT, app_name)
		if not os.path.exists(dest):
			try:
				os.symlink(app_media_dir, dest) # will not work on windows.
				if verbosity > 1:
					print "symlinked app_media dir for app: %s" % app_name
			except:
				# Windows users should get a note, that they should copy the
				# media files to the destination.
				error_msg	= "Failed to link media for '%s'\n" % app_name
				instruction = ("Please copy the media files to the MEDIA_ROOT",
					"manually\n")
				sys.stderr.write(color_style().ERROR(str(error_msg)))
				sys.stderr.write(" ".join(instruction))

signals.post_syncdb.connect(link_app_media)
