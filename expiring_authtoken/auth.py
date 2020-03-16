import datetime
from rest_framework.authentication import SessionAuthentication
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import Token
from rest_framework import HTTP_HEADER_ENCODING
 
# 获取请求头里的token信息
def get_authorization_header(request):
	"""
	Return request's 'Authorization:' header, as a bytestring.
	Hide some test client ickyness where the header can be unicode.
	"""
	auth = request.META.get('HTTP_AUTHORIZATION', b'')
	if isinstance(auth, type('')):
		# Work around django test client oddness
		auth = auth.encode(HTTP_HEADER_ENCODING)
	return auth
 
# 自定义的ExpiringTokenAuthentication认证方式
class ExpiringTokenAuthentication(BaseAuthentication):
	model = Token
	header = 'Token'

	def authenticate(self, request):
		auth = get_authorization_header(request)
 
		if not auth:
			return None
		try:
			token = auth.decode()
		except UnicodeError:
			msg = _('Invalid token header. Token string should not contain invalid characters.')
			raise exceptions.AuthenticationFailed(msg)
		return self.authenticate_credentials(token)
 
	def authenticate_credentials(self, key):
		try:
			key.index(self.header + '=')
		except ValueError:
			return None

		key = key.replace(self.header + '=','',1)

		# 增加了缓存机制
		token_cache_key = 'token_' + key
		cache_user = cache.get(token_cache_key)
		if cache_user:
			return (cache_user.user, cache_user)  # 首先查看token是否在缓存中，若存在，直接返回用户

		try:
			token = self.model.objects.get(pk=key)
		except (self.model.DoesNotExist,ValidationError):
			raise exceptions.AuthenticationFailed('Invalid token.')
 
		if not token.user.is_active:
			raise exceptions.AuthenticationFailed('User is inactive.')
 
		if(timezone.now() - datetime.timedelta(days=settings.TOKEN_EXPIRE_DAYS)) > token.created_time:  # 设定存活时间
			token.delete()
			raise exceptions.AuthenticationFailed('Token expired.')
 
		cache.set(token_cache_key, token, 60 * 60)  # 添加 token_xxx 到缓存
		return (token.user, token)
 
	def authenticate_header(self, request):
		return self.header