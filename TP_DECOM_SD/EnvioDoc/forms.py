from django import forms

from TP_DECOM_SD.usuarios.models import User
from .models import Documento

class DocumentoForm(forms.ModelForm):
    equipe = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(cargo='aluno'),
        required=False,
        widget=forms.CheckboxSelectMultiple(),  # Usando checkboxes para seleção
        help_text="Selecione alunos para incluir na equipe (somente para professores)"
    )

    class Meta:
        model = Documento
        fields = ['titulo', 'autor', 'equipe', 'resumo', 'palavras_chave', 'data_publicacao', 'revista', 'arquivo']
    
    def clean_arquivo(self):
        arquivo = self.cleaned_data.get('arquivo')
        if arquivo:
            if not arquivo.name.endswith('.pdf'):
                raise forms.ValidationError("Apenas arquivos PDF são permitidos.")
        return arquivo
