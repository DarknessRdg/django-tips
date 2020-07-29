from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('imagem', views.ModelComImagemView)
router.register('user', views.UserView)

urlpatterns = [
    path('', include(router.urls))
]
