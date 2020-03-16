from rest_framework import serializers
from django.conf import settings
from .models import *
from django.core.exceptions import ValidationError
from itertools import groupby
from django.utils import timezone
import datetime

'''
class Serializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = 
		fields = '__all__'
'''

class PageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Page
		fields = ['index','word','accent']

class ScoredPageSerializer(serializers.ModelSerializer):
	page = PageSerializer()

	class Meta:
		model = PageLog
		fields = ['page','score']
		depth = 1

class BookSerializer(serializers.ModelSerializer):
	pages = PageSerializer(many=True)
	thumbnail = serializers.ImageField(read_only=True,use_url=True)

	class Meta:
		model = Book
		fields = ['uuid','name','description','pages','thumbnail']

class LogSerializer(serializers.ModelSerializer):
	details = ScoredPageSerializer(source='pagelog_set',many=True)
	timestamp = serializers.SerializerMethodField()

	class Meta:
		model = Log
		fields = ['uuid','date','timestamp','book','details']
		depth = 1

	def get_timestamp(self,obj):
		return int(obj.date.timestamp())

class ProfileSerializer(serializers.ModelSerializer):
	avatar = serializers.ImageField(read_only=True)
	email = serializers.EmailField(source='user.email')

	class Meta:
		model = Profile
		fields = ['nickname','avatar','email']

def limit_avatar_size(value):
	mxsize = settings.MAX_AVATAR_SIZE
	if(mxsize and value.size > mxsize):
		raise ValidationError("Maximum file size(%.1fMB) exceeded." % (mxsize / (1024 * 1024)))
	else:
		return value

class AvatarUploadSerializer(serializers.ModelSerializer):
	file = serializers.ImageField(source='avatar',allow_empty_file=False,validators=(limit_avatar_size,))

	class Meta:
		model = Profile
		fields = ['file']