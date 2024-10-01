from django.urls import path
from .api_views import DocumentoList, DocumentoSearch, DocumentoUpdate, DocumentoCreate, DocumentoDelete

urlpatterns = [
    path('documentos/list', DocumentoList.as_view(), name='documento-list'),
    path('documentos/search/', DocumentoSearch.as_view(), name='documento-search'),
    path('documentos/update/<int:id>', DocumentoUpdate.as_view(), name='documento-update'),
    path('documentos/create/', DocumentoCreate.as_view(), name='documento-create'),  # New create endpoint
    path('documentos/delete/<int:id>', DocumentoDelete.as_view(), name='documento-delete'),  # New delete endpoint
]


#exemplo de query para a busca ?q=teste%20qualquer
