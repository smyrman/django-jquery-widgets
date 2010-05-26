# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings

from jquey_widgets.widgets import ForeignKeySearchInput


class ForeignKeySearchField(forms.fields.ChoiceField):
	"""Form field to select a model for a ForeignKey db field"""
	pass # Fix this field later
