"""djangocrud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('admin_usuarios/<accion>/<id>', views.admin_usuarios, name='admin_usuarios'),
    path('crear_perfil/', views.crear_perfil, name='crear_perfil'),
    path('generate_password/', views.generate_password, name='generate_password'),
    # Agregando nuevas URLs basadas en el diagrama
    path('gestionar_agenda_medica/', views.gestionar_agenda_medica, name='gestionar_agenda_medica'),
    path('gestionar_horas_medicas/', views.gestionar_horas_medicas, name='gestionar_horas_medicas'),
    path('consultar_pacientes_en_espera/', views.consultar_pacientes_en_espera, name='consultar_pacientes_en_espera'),
    path('emitir_informes_transacciones/', views.emitir_informes_transacciones, name='emitir_informes_transacciones'),
    path('ingresar_pagos/', views.ingresar_pagos, name='ingresar_pagos'),
    path('enviar_correos/', views.enviar_correos, name='enviar_correos'),
    path('mis_datos/', views.mis_datos, name='mis_datos'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)