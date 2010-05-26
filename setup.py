# -*- coding: utf-8 -*-
#!/usr/bin/env python

from distutils.core import setup

setup(name='jQuery Widgets',
      version='0.1',
      description='jQuery-powered widgets and fields',
      author='Sindre Røkenes Myren',
      author_email='smyrman@gmail.com',
      url='http://github.com/smyrman/django-jquery-widgets',
      packages=['jquery_widgets', ],
      include_package_data = True, # include everything in source control
)
