from django.contrib import admin
from .models import Atletas, DatosCondicion, TipoEntrenamiento, Ejercicio, PlanEntrenamiento, DetallePlanEntrenamiento

# Inline para Ejercicios en TipoEntrenamiento
class EjercicioInline(admin.TabularInline):
    model = Ejercicio
    extra = 1  # Número de ejercicios adicionales para agregar

# Admin para TipoEntrenamiento con inline de Ejercicios
@admin.register(TipoEntrenamiento)
class TipoEntrenamientoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    inlines = [EjercicioInline]  # Para agregar ejercicios directamente en el tipo de entrenamiento

# Inline para Detalles del Plan de Entrenamiento en PlanEntrenamiento
class DetallePlanEntrenamientoInline(admin.TabularInline):
    model = DetallePlanEntrenamiento
    extra = 1  # Número de detalles adicionales para agregar

# Admin para PlanEntrenamiento con inline de Detalles
@admin.register(PlanEntrenamiento)
class PlanEntrenamientoAdmin(admin.ModelAdmin):
    list_display = ('atleta', 'fecha_creacion', 'fecha_validez', 'tipo_entrenamiento')
    inlines = [DetallePlanEntrenamientoInline]  # Agregar detalles del plan en línea

# Admin para Atletas
@admin.register(Atletas)
class AtletaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'fecha_nacimiento', 'ciudad', 'email')
    search_fields = ('nombre', 'apellido')
    list_filter = ('ciudad',)

# Admin para DetallePlanEntrenamiento
@admin.register(DetallePlanEntrenamiento)
class DetallePlanEntrenamientoAdmin(admin.ModelAdmin):
    list_display = ('plan_entrenamiento', 'ejercicio', 'repeticiones', 'unidad_repeticion', 'series', 'intensidad')