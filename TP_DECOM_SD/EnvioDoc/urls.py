from django.urls import path
from . import views
from .views import Atualizar_forms

urlpatterns = [
    path('', views.index, name='index'),
    path('editar_documento/<int:pk>/', Atualizar_forms.as_view(), name='editar_artigo'),
]

