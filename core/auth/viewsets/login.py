from rest_framework import viewsets
from django.utils import timezone
from core.auth.serializers import AuthSerializer
from core.auth.models import AuthToken
from core.auth.authentication import JWTAuth
from rest_framework import status, response
from rest_framework.permissions import AllowAny


class ObtainAuthToken(viewsets.ViewSet):
    serializer_class = AuthSerializer
    http_method_names = ['post']
    queryset = AuthToken.objects.all()
    permission_classes = (AllowAny,)


    def create(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data, context={'request':request})
        
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.last_login = timezone.now()
        token = JWTAuth().get_token(user)
        user.save()
        return response.Response({'token':token,
                                    'public_id':user.public_id,
                                    'position': user.position,
                                    'first_name': user.first_name,
                                    'last_name': user.last_name}, 
                                    status=status.HTTP_200_OK)


