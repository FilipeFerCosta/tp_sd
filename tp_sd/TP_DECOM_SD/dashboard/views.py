from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from TP_DECOM_SD.EnvioDoc.models import Documento
import matplotlib.pyplot as plt
import io
import base64
from django.db.models import Count
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse

# Verificar se o usuário tem permissão para autorizar ou negar (admin)
def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(lambda u: u.is_staff)
def relatorio_geral(request):
    artigos_aprovados = Documento.objects.filter(aprovado=True)
    artigos_pendentes = Documento.objects.filter(status='pendente')

    return render(
        request, 
        'apps/dashboard/relatorio.html', 
        {'aprovados': artigos_aprovados, 'pendentes': artigos_pendentes}
    )

def generate_chart(data, chart_type):
    """
    Função para gerar gráficos usando matplotlib com proporção ajustada.
    :param data: Dicionário com 'labels' e 'values'.
    :param chart_type: Tipo de gráfico ('pie' ou 'bar').
    :return: String base64 com a imagem gerada.
    """
    # Ajuste do tamanho para proporção 1080x720
    fig, ax = plt.subplots(figsize=(10.8, 7.2))

    if chart_type == 'pie':
        ax.pie(data['values'], labels=data['labels'], autopct='%1.1f%%', startangle=90)
    elif chart_type == 'bar':
        ax.bar(data['labels'], data['values'], color='skyblue')
        ax.set_xlabel('Categorias')
        ax.set_ylabel('Valores')
    else:
        raise ValueError("Tipo de gráfico inválido.")

    # Salvar gráfico como imagem em memória
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100)  # DPI ajustado para garantir qualidade
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close(fig)

    # Converter imagem para base64
    return base64.b64encode(image_png).decode('utf-8')

@login_required
@user_passes_test(is_admin)
def export_articles_pdf(request):
    # Dados de exemplo (substitua pelos dados reais)
    articles = [
        {"title": "Artigo 1", "status": "Publicado", "ano": 2023},
        {"title": "Artigo 2", "status": "Revisão", "ano": 2022},
    ]

    # Gerar os dados para os gráficos
    status_data = {'labels': ['Publicado', 'Revisão'], 'values': [10, 5]}
    status_chart_image = generate_chart(status_data, 'pie')

    ano_data = {'labels': ['2023', '2022'], 'values': [12, 8]}
    ano_chart_image = generate_chart(ano_data, 'bar')

    palavras_data = {'labels': ['Python', 'Django'], 'values': [7, 5]}
    palavras_chart_image = generate_chart(palavras_data, 'bar')

    equipe_data = {'labels': ['Equipe A', 'Equipe B'], 'values': [9, 6]}
    equipe_chart_image = generate_chart(equipe_data, 'pie')

    # Renderizar o HTML com as imagens dos gráficos
    html_string = render_to_string('apps/dashboard/dashboard.html', {
        'articles': articles,
        'status_chart_image': status_chart_image,
        'ano_chart_image': ano_chart_image,
        'palavras_chart_image': palavras_chart_image,
        'equipe_chart_image': equipe_chart_image,
    })

    # Gerar o PDF a partir do HTML renderizado
    pdf_file = HTML(string=html_string).write_pdf()

    # Enviar o PDF como resposta
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_artigos.pdf"'
    return response

@login_required
@user_passes_test(is_admin)
def autorizar_artigo(request, artigo_id):
    """
    Autoriza o artigo com o id fornecido.
    """
    artigo = get_object_or_404(Documento, id=artigo_id)
    
    # Atualiza o estado do artigo para autorizado (aprovado)
    artigo.aprovado = True
    artigo.status = 'aprovado'  # Supondo que você tenha um campo de status
    artigo.save()
    
    # Exibe uma mensagem de sucesso
    messages.success(request, 'Artigo autorizado com sucesso!')
    
    # Redireciona de volta para a página de artigos pendentes ou onde preferir
    return redirect('relatorio_geral')

@login_required
@user_passes_test(is_admin)
def negar_artigo(request, artigo_id):
    """
    Nega o artigo com o id fornecido.
    """
    artigo = get_object_or_404(Documento, id=artigo_id)
    
    # Atualiza o estado do artigo para negado
    artigo.aprovado = False
    artigo.status = 'negado'  # Supondo que você tenha um campo de status
    artigo.save()
    
    # Exibe uma mensagem de erro ou negação
    messages.error(request, 'Artigo negado!')
    
    # Redireciona de volta para a página de artigos pendentes ou onde preferir
    return redirect('relatorio_geral')

@login_required
@user_passes_test(lambda u: u.is_staff)
def relatorio_grafico(request):
    # Gráfico 1: Contagem de documentos por status
    status_count = Documento.objects.values('status').annotate(count=Count('status'))

    # Gráfico 2: Contagem de documentos por ano
    ano_count = Documento.objects.values('data_publicacao').annotate(count=Count('data_publicacao')).order_by('data_publicacao')

    # Gráfico 3: Contagem de documentos por palavras-chave
    palavras_count = Documento.objects.values('palavras_chave').annotate(count=Count('palavras_chave')).order_by('-count')[:10]  # Top 10 palavras-chave

    # Gráfico 4: Contagem de documentos por equipe
    equipe_count = Documento.objects.values('equipe').annotate(count=Count('equipe')).order_by('-count')

    context = {
        'status_count': status_count,
        'ano_count': ano_count,
        'palavras_count': palavras_count,
        'equipe_count': equipe_count,
    }
    
    return render(request, 'apps/dashboard/dashboard.html', context)



