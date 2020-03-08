from rest_framework.serializers import ModelSerializer
from .models import *


class ModelComImagemSerializer(ModelSerializer):
    class Meta:
        model = ModelComImagem
        fields = '__all__'  # todos os campos (atributos) do model ModelComImagem
