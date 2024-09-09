from django import forms
from .models import Documento

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['titulo', 'autores', 'resumo', 'palavras_chave', 'data_publicacao', 'revista', 'arquivo']
    
    def clean_arquivo(self):
        arquivo = self.cleaned_data.get('arquivo')
        if arquivo:
            if not arquivo.name.endswith('.pdf'):
                raise forms.ValidationError("Apenas arquivos PDF são permitidos.")
        return arquivo
