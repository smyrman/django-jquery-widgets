# -*- coding: utf-8 -*-
#!/usr/bin/env python

from distutils.core import setup
VERSION = '0.1.1'

setup(name='django-jquery-widgets',
	version=VERSION,
	description='jQuery-powered widgets and fields for Django',
	author='Sindre Røkenes Myren',
	author_email='smyrman@gmail.com',
	url='http://github.com/smyrman/django-jquery-widgets',
	install_requires='django >= 1.1',
	download_url='http://github.com/smyrman/django-jquery-widgets/tarball/%s'%VERSION,
	packages=['jquery_widgets'],
	package_data={'jquery_widgets': ['media/js/*.js', 'media/css/*.css']},
)
