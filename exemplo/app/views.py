from rest_framework import viewsets
from . import models, serializers


class ModelComImagemView(viewsets.ModelViewSet):
    queryset = models.ModelComImagem.objects.all()
    serializer_class = serializers.ModelComImagemSerializer
