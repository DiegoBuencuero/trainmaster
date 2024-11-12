from django.utils import timezone
from django.db import models
from decimal import Decimal, InvalidOperation


class Atletas(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    fecha_registro = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class DatosCondicion(models.Model):
    atleta = models.ForeignKey(Atletas, on_delete=models.CASCADE, related_name='datos_condicion')
    fecha_medicion = models.DateField(auto_now_add=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2)  # Ej. 70.50 kg
    altura = models.DecimalField(max_digits=5, decimal_places=2)  # Ej. 175.50 cm
    imc = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # Calculado
    circunferencia_cintura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    circunferencia_cadera = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    nivel_condicion_fisica = models.CharField(max_length=50, choices=[
        ('novato', 'Novato'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado')
    ])
    objetivo_entrenamiento = models.CharField(max_length=100)
    historial_lesiones = models.TextField(null=True, blank=True)
    frecuencia_entrenamiento = models.PositiveIntegerField()  # Ej. 3 (entrenamientos por semana)
    nivel_actividad_diaria = models.CharField(max_length=50, choices=[
        ('sedentario', 'Sedentario'),
        ('activo', 'Activo'),
        ('muy_activo', 'Muy Activo')
    ])

    def __str__(self):
        return f"Datos de {self.atleta.nombre} {self.atleta.apellido} - {self.fecha_medicion}"

    def calcular_imc(self):
        if self.peso and self.altura:
            try:
                altura_metros = self.altura / Decimal(100)  # Convertir a metros
                self.imc = self.peso / (altura_metros ** 2)
            except (InvalidOperation, ZeroDivisionError):
                self.imc = None


class TipoEntrenamiento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Ejercicio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    tipo_entrenamiento = models.ForeignKey(TipoEntrenamiento, on_delete=models.CASCADE, related_name='ejercicios')

    def __str__(self):
        return self.nombre

class PlanEntrenamiento(models.Model):
    atleta = models.ForeignKey(Atletas, on_delete=models.CASCADE, related_name='planes_entrenamiento')
    fecha_creacion = models.DateField(default=timezone.now)
    fecha_validez = models.DateField()
    tipo_entrenamiento = models.ForeignKey(TipoEntrenamiento, on_delete=models.CASCADE, related_name='planes')

    def __str__(self):
        return f"Plan de {self.atleta} - {self.tipo_entrenamiento.nombre} - {self.fecha_creacion}"

class DetallePlanEntrenamiento(models.Model):
    INTENSIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('maxima', 'Máxima'),
    ]

    UNIDAD_REPETICION_CHOICES = [
        ('repeticiones', 'Repeticiones'),
        ('tiempo', 'Tiempo (segundos)'),
        ('peso', 'Peso (kg)'),
    ]

    plan_entrenamiento = models.ForeignKey(PlanEntrenamiento, on_delete=models.CASCADE, related_name='detalles')
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    repeticiones = models.PositiveIntegerField()
    unidad_repeticion = models.CharField(max_length=20, choices=UNIDAD_REPETICION_CHOICES, default='repeticiones')
    series = models.PositiveIntegerField()
    intensidad = models.CharField(max_length=50, choices=INTENSIDAD_CHOICES)

    def __str__(self):
        return f"{self.ejercicio.nombre} - {self.repeticiones} reps, {self.series} series"
