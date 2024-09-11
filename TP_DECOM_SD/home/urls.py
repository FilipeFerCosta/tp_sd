from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='busca_documentos'),
    path('/<int:documento_id>/', views.visualizar_documento, name='visualizar_documento'),
    path('/<int:documento_id>/deletar/', views.deletar_documento, name='deletar_documento'),

]

