from django.contrib import admin
from django.urls import path
from landing.views import home, abm_atletas, ajax_get_atletas_data, cargar_condiciones, crear_plan_entrenamiento, ajax_get_ejercicios,  ajax_get_tipos_ejercicio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('abm_atletas/', abm_atletas, name='abm_atletas'),
    path('ajax_get_atletas_data/', ajax_get_atletas_data, name='ajax_get_atletas_data'),
    path('cargar_condiciones/', cargar_condiciones, name='cargar_condiciones'),
    path('crear_plan_entrenamiento/', crear_plan_entrenamiento, name='crear_plan_entrenamiento'),
    path('ajax_get_tipos_ejercicio/',ajax_get_tipos_ejercicio, name='ajax_get_tipos_ejercicio'),
    path('ajax_get_ejercicios/', ajax_get_ejercicios, name='ajax_get_ejercicios'),
]
