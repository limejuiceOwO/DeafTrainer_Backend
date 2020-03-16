from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Book)
admin.site.register(Page)
admin.site.register(Log)
admin.site.register(PageLog)
admin.site.register(Profile)
admin.site.register(Slogan)