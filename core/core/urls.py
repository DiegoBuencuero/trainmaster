"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from landing.views import home,abm_atletas, ajax_get_usuario_data,cargar_condiciones
print("URLs cargadas correctamente") 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('abm_atletas/', abm_atletas, name='abm_atletas'),
    path('ajax_get_usuario_data/', ajax_get_usuario_data, name='ajax_get_usuario_data'),
     path('cargar_condiciones/', cargar_condiciones, name='cargar_condiciones'),
]