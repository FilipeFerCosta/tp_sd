from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from TP_DECOM_SD.EnvioDoc.models import Documento
from .serializers import DocumentoSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import generics


class DocumentoCreate(generics.CreateAPIView):
    """
    View para criar um novo documento.

    POST:
    Cria um novo documento com base nos dados fornecidos no corpo da requisição.

    Retorno:
    - 201 Created: Documento criado com sucesso.
    - 400 Bad Request: Dados inválidos fornecidos.
    """
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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

class DocumentoUpdate(APIView):
    """
    View para atualizar um documento específico ou retornar seus dados.

    GET:
    Retorna os dados do documento a ser atualizado.

    PUT/PATCH:
    Atualiza o documento com os dados fornecidos.

    Parâmetro de URL:
    - id: O ID do documento a ser atualizado.

    Retorno:
    - 200 OK: Documento atualizado com sucesso ou dados do documento.
    - 404 Not Found: Documento não encontrado.
    - 400 Bad Request: Dados inválidos fornecidos.
    """

    def get(self, request, id):
        documento = get_object_or_404(Documento, id=id)
        serializer = DocumentoSerializer(documento)
        return Response(serializer.data)

    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer

    def put(self, request, id):

        documento = get_object_or_404(Documento, id=id)
        serializer = DocumentoSerializer(documento)
        
        # Recuperar o documento existente baseado no ID fornecido
        documento = get_object_or_404(Documento, id=id)

        # Passar os dados atualizados para o serializer, junto com a instância existente
        serializer = DocumentoSerializer(documento, data=request.data)  # Use o serializer diretamente

        if serializer.is_valid():
            serializer.save()  # Salva as mudanças no documento
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DocumentoDelete(APIView):
    """
    View para excluir um documento específico.

    DELETE:
    Exclui o documento correspondente ao ID fornecido.

    Parâmetro de URL:
    - id: O ID do documento a ser excluído.

    Retorno:
    - 204 No Content: Documento excluído com sucesso.
    - 404 Not Found: Documento não encontrado.
    """
    def delete(self, request, id):
        documento = get_object_or_404(Documento, id=id)
        documento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)