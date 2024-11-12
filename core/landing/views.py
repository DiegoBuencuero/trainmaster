from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Atletas, DatosCondicion, DetallePlanEntrenamiento, Ejercicio, TipoEntrenamiento
from .forms import AtletaForm, DatosCondicionForm, DetallePlanEntrenamientoForm, PlanEntrenamientoForm
from datetime import date
from django.forms import modelformset_factory
from django import template


#@login_required
def home(request):
    print("La vista 'home' se está ejecutando")
    return render(request, 'index.html')


def abm_atletas(request):
    atletas = Atletas.objects.all()  # Obtener todos los atletas para listarlos en la tabla

    if request.method == 'POST':
        registro_id = request.POST.get('registro_id')  # ID del atleta a editar o eliminar

        if registro_id:
            # Si hay un ID de atleta, se realiza una edición
            atleta_instance = Atletas.objects.get(id=registro_id)
            form = AtletaForm(data=request.POST, files=request.FILES, instance=atleta_instance)
        else:
            # Si no hay ID, se crea un nuevo registro
            form = AtletaForm(data=request.POST, files=request.FILES)
        
        if form.is_valid():
            if 'eliminar' in request.POST:
                atleta_instance.delete()
            else:
                form.save()  # Guardar (actualizar o crear nuevo)
            form = AtletaForm()  # Reiniciar el formulario después de guardar
    else:
        form = AtletaForm()  # Formulario vacío al cargar la página

    return render(request, 'abm_atletas.html', {'form': form, 'atletas': atletas})

def ajax_get_atletas_data(request):
    try:
        atleta_id = int(request.GET.get('atleta'))
        atleta = Atletas.objects.get(id=atleta_id)

        # Datos para rellenar el formulario de edición
        data = {
            'nombre': atleta.nombre,
            'apellido': atleta.apellido,
            'fecha_nacimiento': atleta.fecha_nacimiento.strftime('%Y-%m-%d'),
            'direccion': atleta.direccion,
            'ciudad': atleta.ciudad,
            'telefono': atleta.telefono,
            'email': atleta.email,
            'fecha_registro': atleta.fecha_registro.strftime('%Y-%m-%d')
        }
        
        return JsonResponse({'response': 0, 'data': data})
    except Atletas.DoesNotExist:
        return JsonResponse({'response': 1, 'data': None})

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

    atletas = Atletas.objects.all()  # Lista de atletas para seleccionar
    return render(request, 'cargar_condiciones.html', {'form': form, 'atletas': atletas})

def crear_plan_entrenamiento(request):
    DetalleFormSet = modelformset_factory(DetallePlanEntrenamiento, form=DetallePlanEntrenamientoForm, extra=5, can_delete=True)
    if request.method == 'POST':
        plan_form = PlanEntrenamientoForm(request.POST)
        detalle_formset = DetalleFormSet(request.POST, queryset=DetallePlanEntrenamiento.objects.none())

        if plan_form.is_valid() and detalle_formset.is_valid():
            plan = plan_form.save()
            for detalle_form in detalle_formset:
                detalle = detalle_form.save(commit=False)
                detalle.plan_entrenamiento = plan
                detalle.save()
            return redirect('lista_planes_entrenamiento')
    else:
        plan_form = PlanEntrenamientoForm()
        detalle_formset = DetalleFormSet(queryset=DetallePlanEntrenamiento.objects.none())

    context = {
        'plan_form': plan_form,
        'detalle_formset': detalle_formset,
        'atletas': Atletas.objects.all(),
    }
    return render(request, 'entrenamiento_crear_plan.html', context)


def ajax_get_tipos_ejercicio(request):
    tipo_entrenamiento_id = request.GET.get('tipo_entrenamiento_id')
    tipos_ejercicio = TipoEntrenamiento.objects.filter(id=tipo_entrenamiento_id).values('id', 'nombre')
    data = list(tipos_ejercicio)
    return JsonResponse({'tipos_ejercicio': data})

def ajax_get_ejercicios(request):
    tipo_entrenamiento_id = request.GET.get('tipo_entrenamiento_id')
    ejercicios = Ejercicio.objects.filter(tipo_entrenamiento_id=tipo_entrenamiento_id)
    ejercicios_data = [{'id': ejercicio.id, 'nombre': ejercicio.nombre} for ejercicio in ejercicios]
    return JsonResponse({'ejercicios': ejercicios_data})