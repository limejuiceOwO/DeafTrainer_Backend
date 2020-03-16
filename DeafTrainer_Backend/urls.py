"""DeafTrainer_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import *
from django.conf.urls import url
from expiring_authtoken.views import *

from .settings import MEDIA_ROOT
from django.views.static import serve

urlpatterns = [
	path('api/', include('dt.urls')),
    path('api-auth/', obtain_auth_token),
    path('api-auth/logout', destroy_auth_token),
    path('api-auth/renew', renew_auth_token),
    path('admin/', admin.site.urls),
    path('rest/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),#DEV ONLY
]
