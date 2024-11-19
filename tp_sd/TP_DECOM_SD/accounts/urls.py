# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views 
from . views import ListaRegistrosAuditoria, login_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register_view, name='register'),  # View personalizada para registro
    path('registros-auditoria/', ListaRegistrosAuditoria.as_view(), name='registros_auditoria'),
]
