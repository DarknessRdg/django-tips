from django.db import models


class ModelComImagem(models.Model):
    imagem = models.ImageField(upload_to='pasta_das_imagens/')
