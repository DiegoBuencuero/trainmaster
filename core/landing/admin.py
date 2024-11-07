from django.contrib import admin
from .models import Atleta, DatosCondicion


class DatosCondicionInline(admin.TabularInline):
    model = DatosCondicion
    extra = 1
    readonly_fields = ('fecha_medicion', 'imc')  # Hace que `imc` y `fecha_medicion` sean solo lectura
    fields = ('fecha_medicion', 'peso', 'altura', 'circunferencia_cintura', 'circunferencia_cadera', 
              'nivel_condicion_fisica', 'objetivo_entrenamiento', 'historial_lesiones', 
              'frecuencia_entrenamiento', 'nivel_actividad_diaria', 'imc')
class AtletaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'fecha_nacimiento', 'ciudad', 'email')
    search_fields = ('nombre', 'apellido')
    list_filter = ('ciudad',)
    inlines = [DatosCondicionInline]  # Incluye el inline para mostrar los registros de condición física

admin.site.register(Atleta, AtletaAdmin)