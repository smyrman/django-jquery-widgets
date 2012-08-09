# -*- coding: utf-8 -*-
from django import forms

from .widgets import JQWSlider


class ForeignKeySearchField(forms.fields.ChoiceField):
	"""Form field to select a model for a ForeignKey db field"""
	pass # Fix this field later


class JQWSliderField(forms.IntegerField):
	
	def __init__(self, min_value, max_value, step=1, **kwargs):
		self.step = step
		kwargs.update({'widget': JQWSlider})
		super(JQWSliderField, self).__init__(max_value, min_value, **kwargs)
		
	def widget_attrs(self, widget):
		widget.min_value = self.min_value
		widget.max_value = self.max_value
		widget.step = self.step