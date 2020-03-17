#from django.shortcuts import render
from time import sleep
#from django.views import View
from rest_framework import viewsets,permissions,authentication,mixins,parsers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .serializers import *
from .models import *
from expiring_authtoken.auth import ExpiringTokenAuthentication

'''
class ViewSet(viewsets.ModelViewSet):
	queryset = 
	serializer_class = Serializer
	permission_classes = []
'''

class BookViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Book.objects.all().order_by('name')
	serializer_class = BookSerializer

class LogViewSet(mixins.DestroyModelMixin,
				viewsets.ReadOnlyModelViewSet):
	serializer_class = LogSerializer
	authentication_classes = (
		ExpiringTokenAuthentication,
		authentication.SessionAuthentication,
	)
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		return self.request.user.log_set;

class ProfileView(APIView):
	serializer_class = ProfileSerializer
	authentication_classes = (
		ExpiringTokenAuthentication,
		authentication.SessionAuthentication,
	)
	permission_classes = (permissions.IsAuthenticated,)
	parser_classes = (parsers.JSONParser,)

	def get(self,request,*args,**kwargs):
		serializer = self.serializer_class(request.user.profile,context={"request" : request})
		return Response(serializer.data)

	def put(self,request,*args,**kwargs):
		serializer = self.serializer_class(request.user.profile,data=request.data)
		serializer.is_valid(raise_exception=True)
		new_model = serializer.save()
		new_model.save()
		return Response({"detail":"Update succeed."})

class AvatarUploadView(APIView):
	serializer_class = AvatarUploadSerializer
	authentication_classes = (
		ExpiringTokenAuthentication,
		authentication.SessionAuthentication,
		authentication.BasicAuthentication,#DEV ONLY
	)
	permission_classes = (permissions.IsAuthenticated,)
	parser_classes = (parsers.FileUploadParser,)

	def post(self,request,*args,**kwargs):
		serializer = self.serializer_class(request.user.profile,data=request.data)
		serializer.is_valid(raise_exception=True)
		new_model = serializer.save()
		new_model.save()
		return Response({"detail":"Upload succeed."})

class HomepageView(APIView):
	authentication_classes = (
		ExpiringTokenAuthentication,
		authentication.SessionAuthentication,
		authentication.BasicAuthentication,#DEV ONLY
	)
	permission_classes = (permissions.IsAuthenticated,)

	def get(self,request,*args,**kwargs):
		#sleep(2)
		obj = request.user.profile
		res = {}
		if(obj.current_book):
			res['book_uuid'] = obj.current_book.uuid
			res['book_name'] = obj.current_book.name
			res['words_total'] = obj.current_book.pages.count()
			res['words_learned'] = len(list(groupby(
				PageLog.objects.filter(log__book=obj.current_book,log__user=obj.user).order_by('page__index'),
				key=lambda x:x.page.index
			)))

		now = datetime.datetime.now()
		today = timezone.make_aware(datetime.datetime(
			now.year,
			now.month,
			now.day
		))
		print(today - datetime.timedelta(now.isoweekday()))
		now = timezone.make_aware(now)
		res['today_learned'] = PageLog.objects.filter(log__user=obj.user,log__date__gt=today).count()
		res['week_learned'] = PageLog.objects.filter(log__user=obj.user,log__date__gt=today - datetime.timedelta(now.isoweekday())).count()
		res['hist_learned'] = [PageLog.objects.filter(
			log__user=obj.user,
			log__date__gt=today - datetime.timedelta(days=day + 1),
			log__date__lte=today - datetime.timedelta(days=day)
		).count() for day in range(0,7)]

		return Response(res)