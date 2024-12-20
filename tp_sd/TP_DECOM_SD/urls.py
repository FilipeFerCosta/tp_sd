from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('TP_DECOM_SD.home.urls')),  
    path('documentos/', include('TP_DECOM_SD.EnvioDoc.urls')),  
    path('api/', include('TP_DECOM_SD.API.urls')),  
    path('accounts/', include('TP_DECOM_SD.accounts.urls')),
    path('dashboard/', include('TP_DECOM_SD.dashboard.urls')),
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # Rotas para arquivos estáticos e mídia no modo de desenvolvimento
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)