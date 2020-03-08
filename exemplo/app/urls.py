from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('imagem', views.ModelComImagemView)

urlpatterns = [
    path('', include(router.urls))
]
