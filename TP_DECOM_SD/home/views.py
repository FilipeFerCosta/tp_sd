from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.core.paginator import Paginator
from TP_DECOM_SD.EnvioDoc.models import Documento

def index(request):
   
    termo_busca = request.GET.get('q', '')

    
    if termo_busca:
        documentos = Documento.objects.filter(
            Q(titulo__icontains=termo_busca) |
            Q(autores__icontains=termo_busca) |
            Q(revista__icontains=termo_busca) |
            Q(palavras_chave__icontains=termo_busca) |
            Q(resumo__icontains=termo_busca) |
            Q(data_publicacao__icontains=termo_busca)
        )
    else:
        documentos = Documento.objects.all()

   
    ordenacao = request.GET.get('ordenacao', 'titulo')
    documentos = documentos.order_by(ordenacao)

    paginator = Paginator(documentos, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'documentos': page_obj,
        'page_obj': page_obj,
        'query': termo_busca,
        'ordenacao': ordenacao,
    }

    return render(request, 'busca_documentos.html', context)

def visualizar_documento(request, documento_id):
    
    try:
        documento = Documento.objects.filter(pk=documento_id)
    except documento.DoesNotExist:
        raise Http404('Documento Não Existe') # type: ignore
    context = {
        'documento' : documento
        } 
    return render(request, 'visualizar_documento.html', context)


def deletar_documento(request, documento_id):
    documento = get_object_or_404(Documento, pk=documento_id)

    if request.method == 'POST':
        documento.delete()
        messages.success(request, 'Documento excluído com sucesso!')
        return redirect('busca_documentos')
    
    return render(request, 'deletar_documento.html', {'documento': documento})
