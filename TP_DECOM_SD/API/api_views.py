from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from TP_DECOM_SD.EnvioDoc.models import Documento
from .serializers import DocumentoSerializer

class DocumentoList(APIView):
    """
    View para listar todos os documentos cadastrados no sistema.

    GET:
    Retorna uma lista de todos os documentos disponíveis no banco de dados.

    Retorno:
    - 200 OK: Uma lista de documentos no formato JSON.
    """
    def get(self, request):
        documentos = Documento.objects.all()
        serializer = DocumentoSerializer(documentos, many=True)
        return Response(serializer.data)


class DocumentoSearch(APIView):
    """
    View para buscar documentos com base em um termo de pesquisa.

    Parâmetro de consulta:
    - q: String contendo o termo de busca. A busca é realizada em campos como título, autores, revista, palavras-chave, resumo e data de publicação.

    GET:
    Retorna uma lista de documentos que correspondem ao termo de pesquisa ou todos os documentos caso nenhum termo seja fornecido.

    Retorno:
    - 200 OK: Uma lista de documentos que correspondem ao termo de pesquisa no formato JSON.
    """
    def get(self, request):
        query = request.GET.get('q', '')
        if query:
            documentos = Documento.objects.filter(
                Q(titulo__icontains=query) |
                Q(autores__icontains=query) |
                Q(revista__icontains=query) |
                Q(palavras_chave__icontains=query) |
                Q(resumo__icontains=query) |
                Q(data_publicacao__icontains=query)
            )
        else:
            documentos = Documento.objects.all()  # Se não houver query, retorna todos os documentos

        serializer = DocumentoSerializer(documentos, many=True)
        return Response(serializer.data)
