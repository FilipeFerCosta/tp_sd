from django.urls import path
from . import views
from .views import Atualizar_forms

urlpatterns = [
    path('', views.index, name='criar_documento'),
    path('editar_documento/<int:pk>/', Atualizar_forms.as_view(), name='editar_artigo'),
]

