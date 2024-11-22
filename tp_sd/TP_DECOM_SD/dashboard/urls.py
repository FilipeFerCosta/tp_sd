from django.urls import path
from .views import relatorio_geral,export_articles_pdf,autorizar_artigo,negar_artigo,relatorio_grafico

urlpatterns = [
    path('', relatorio_geral, name='relatorio_geral'),
    path('dashboard/', relatorio_grafico, name='dashboard'),
    path('autorizar/<int:artigo_id>/', autorizar_artigo, name='autorizar_artigo'),
    path('negar/<int:artigo_id>/', negar_artigo, name='negar_artigo'),
    path('export_pdf/', export_articles_pdf, name='export_articles_pdf'),
]


