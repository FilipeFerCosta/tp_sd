from django.urls import path
from .views import DocumentoListView, DocumentoDetailView, DocumentoDeleteView, UserListView, HomePage

urlpatterns = [
    path("", HomePage.as_view(), name="homepage"),
    path('index', DocumentoListView.as_view(), name='listar_documentos'),
    path('documento/<int:documento_id>/', DocumentoDetailView.as_view(), name='visualizar_documento'),
    path('documento/<int:documento_id>/deletar/', DocumentoDeleteView.as_view(), name='deletar_documento'),
    path('usuarios/', UserListView.as_view(), name='listar_usuarios'),
]