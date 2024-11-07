from django import forms
from .models import Atleta, DatosCondicion
from django.utils import timezone

class AtletaForm(forms.ModelForm):
    class Meta:
        model = Atleta
        fields = "__all__"
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'fecha_registro': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'fecha_registro' in self.fields and not self.instance.pk:
            self.fields['fecha_registro'].initial = timezone.now().date()

class DatosCondicionForm(forms.ModelForm):
    class Meta:
        model = DatosCondicion
        fields = [
            'atleta', 'peso', 'altura', 'circunferencia_cintura', 'circunferencia_cadera', 
            'nivel_condicion_fisica', 'objetivo_entrenamiento', 'historial_lesiones', 
            'frecuencia_entrenamiento', 'nivel_actividad_diaria', 'imc'
        ]
        widgets = {
            'atleta': forms.Select(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'placeholder': 'Ej: 70.50', 'id': 'id_peso'}),
            'altura': forms.NumberInput(attrs={'placeholder': 'Ej: 175.50', 'id': 'id_altura'}),
            'imc': forms.NumberInput(attrs={'readonly': 'readonly', 'id': 'id_imc'}),  # Campo solo lectura
            # Otros widgets...
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['imc'].required = False  # Asegura que el campo IMC no sea requerido en el formulario