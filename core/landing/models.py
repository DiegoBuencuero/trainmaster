from django.utils import timezone
from django.db import models
from decimal import Decimal, InvalidOperation


class Atleta(models.Model):
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
    atleta = models.ForeignKey(Atleta, on_delete=models.CASCADE, related_name='datos_condicion')
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