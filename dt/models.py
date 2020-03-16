from django.db.models import *
#from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
import uuid,os

from .fields import *
from .storages import *

# Create your models here.
class Book(Model):
	uuid = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = CharField(max_length=64)
	description = TextField()
	thumbnail = ImageField(upload_to='thumbnail')

class Page(Model):
	book = ForeignKey('Book',on_delete=CASCADE,related_name='pages')
	index = IntegerField()
	word = CharField(max_length=64)
	accent = CharField(max_length=64)
	#res_url = ArrayField()

class Log(Model):
	uuid = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE)
	date = DateTimeField(default=timezone.now)
	book = ForeignKey('Book',on_delete=CASCADE)
	pages = ManyToManyField('Page',through='PageLog')

class PageLog(Model):
	log = ForeignKey('Log',on_delete=CASCADE)
	page = ForeignKey('Page',on_delete=CASCADE)
	score = IntegerField()

class Study(Model):
	user = ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE)
	date = DateTimeField(default=timezone.now)
	book = ForeignKey('Book',on_delete=CASCADE)
	pages_suggestion = ArrayField(converter=int)

def get_avatar_path(instance,filename):
	suffix = filename.split('.')[-1]
	return os.path.join('avatar',instance.user.username,'avatar.' + suffix)

class Profile(Model):
	user = OneToOneField(settings.AUTH_USER_MODEL,on_delete=CASCADE)
	nickname = CharField(max_length=64)
	avatar = ImageField(upload_to=get_avatar_path,storage=OverwriteStorage())
	current_book = ForeignKey('Book',on_delete=SET_NULL,null=True)

class Slogan(Model):
	content = TextField()