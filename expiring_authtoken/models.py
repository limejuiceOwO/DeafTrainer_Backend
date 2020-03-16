from django.db.models import *
from django.conf import settings
from django.utils import timezone
import uuid

# Create your models here.

class Token(Model):
	token = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = OneToOneField(settings.AUTH_USER_MODEL,on_delete=CASCADE, editable=False)
	created_time = DateTimeField(default=timezone.now)