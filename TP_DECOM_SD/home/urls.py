from django.urls import path
from .views import DocumentoListView, DocumentoDetailView, DocumentoDeleteView

urlpatterns = [
    path('', DocumentoListView.as_view(), name='busca_documentos'),
    path('documento/<int:documento_id>/', DocumentoDetailView.as_view(), name='visualizar_documento'),
    path('documento/<int:documento_id>/deletar/', DocumentoDeleteView.as_view(), name='deletar_documento'),
]
