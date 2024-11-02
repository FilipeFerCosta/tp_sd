from django.contrib import admin
from .models import Documento  

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data_publicacao', 'revista')  
    search_fields = ('titulo', 'autor', 'revista')  
    list_filter = ('data_publicacao', 'revista') 
