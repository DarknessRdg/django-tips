from rest_framework import viewsets
from django.contrib.auth.models import User
from . import models, serializers
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    authentication_classes = [JWTAuthentication]


class ModelComImagemView(viewsets.ModelViewSet):
    queryset = models.ModelComImagem.objects.all()
    serializer_class = serializers.ModelComImagemSerializer
