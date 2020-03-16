from django.db import models
from collections import Iterable

class ArrayField(models.Field):

	def __init__(self,seperator=',',converter=None,*args,**kwargs):
		self.sep = seperator
		self.conv = converter
		super().__init__(*args,**kwargs)

	def deconstruct(self):
		name, path, args, kwargs = super().deconstruct()
		if(self.sep != ','):
			kwargs['seperator'] = self.sep
		if(self.conv is not None):
			kwargs['converter'] = self.conv
		return name,path,args,kwargs

	def from_db_value(self, value, expression, connection):
		if value is None:
			return value
		return self.parse(value)

	def to_python(self, value):
		if isinstance(value, list):
			return value
		if value is None:
			return value
		return self.parse(value)

	def get_prep_value(self, value):
		if(value is None):
			return value
		if(not isinstance(value,Iterable)):
			raise TypeError()
		return self.sep.join([str(v) for v in value])

	def get_internal_type(self):
		return 'TextField'

	def value_to_string(self, obj):
		value = self.value_from_object(obj)
		return self.get_prep_value(value)

	def parse(self,value):
		if(not isinstance(value,str)):
			raise TypeError()
		res = value.split(self.sep)
		if(self.conv is not None):
			return [self.conv(v) for v in res]
		else:
			return res