from rest_framework import parsers, renderers
from .auth import ExpiringTokenAuthentication
from .models import Token
from .serializers import AuthTokenSerializer
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.utils import timezone

class ObtainAuthToken(APIView):
	# Copied from rest_framework.authtoken.view
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.token})

class DestroyAuthToken(APIView):
    authentication_classes = (ExpiringTokenAuthentication,)
    throttle_classes = ()
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        token_cache_key = 'token_' + str(request.user.token.token)
        cache.delete(token_cache_key)
        request.user.token.delete()
        return Response({'detail': 'Logout succeed.'})

class RenewAuthToken(APIView):
    authentication_classes = (ExpiringTokenAuthentication,)
    throttle_classes = ()
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        request.user.token.created_time = timezone.now()
        request.user.token.save()
        return Response({'detail': 'Renew succeed.'})

obtain_auth_token = ObtainAuthToken.as_view()
destroy_auth_token = DestroyAuthToken.as_view()
renew_auth_token = RenewAuthToken.as_view()