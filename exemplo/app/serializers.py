from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import *


class ModelComImagemSerializer(ModelSerializer):
    class Meta:
        model = ModelComImagem
        fields = '__all__'  # todos os campos (atributos) do model ModelComImagem


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)