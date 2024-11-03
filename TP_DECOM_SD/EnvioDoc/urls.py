from django.urls import path
from . import views
from .views import DocumentoUpdateView, DocumentoCreateView

urlpatterns = [
    path('', DocumentoCreateView.as_view(), name='index'),
    path('editar_documento/<int:pk>/', DocumentoUpdateView.as_view(), name='editar_artigo'),
]

