from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Atleta, DatosCondicion
from .forms import AtletaForm, DatosCondicionForm
from django.urls import reverse
from datetime import date

#@login_required
def home(request):
    print("La vista 'home' se está ejecutando")
    return render(request, 'index.html')

def abm_atletas(request):
    if request.method == 'POST':
        form = AtletaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('abm_atletas')  # Redirige para evitar recargar el formulario con los mismos datos
        else:
            print(form.errors)  # Para que puedas ver los errores en la consola
    else:
        form = AtletaForm()
    return render(request, 'abm_atletas.html', {'form': form})

#@login_required
def ajax_get_usuario_data(request):
    try:
        usuario_id = int(request.GET.get('usuario'))
        usuario = Atleta.objects.get(id=usuario_id)
        
        # Recopilación de datos básicos del usuario
        u_data = {
            key: value for key, value in usuario.__dict__.items()
            if isinstance(value, (int, str, bool, float))
        }
        
        data = {'response': 0, 'data': u_data}
    except Atleta.DoesNotExist:
        data = {'response': 1, 'data': None}
    return JsonResponse(data)

def cargar_condiciones(request):
    if request.method == 'POST':
        form = DatosCondicionForm(request.POST)
        if form.is_valid():
            datos_condicion = form.save(commit=False)
            datos_condicion.calcular_imc()  # Calcula el IMC automáticamente
            datos_condicion.save()
            return redirect('abm_atletas')  # Redirige a la vista de atletas tras guardar
    else:
        form = DatosCondicionForm()

    usuarios = Atleta.objects.all()  # Lista de atletas para seleccionar
    return render(request, 'cargar_condiciones.html', {'form': form, 'usuarios': usuarios})