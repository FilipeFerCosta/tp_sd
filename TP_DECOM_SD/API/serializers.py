from rest_framework import serializers
from TP_DECOM_SD.EnvioDoc.models import Documento

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__' 
