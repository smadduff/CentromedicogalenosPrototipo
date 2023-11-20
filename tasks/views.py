from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.crypto import get_random_string
from tasks.tools import eliminar_registro
from .models import Perfil
from django.contrib import messages
from .forms import ActualizacionClienteForm, PerfilForm, PerfilFormParaMisDatos, RegistroAdminForm
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})




def home(request):
    return render(request, 'home.html')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('home')




def admin_usuarios(request, accion, id):
    if request.method == 'POST':
        if accion == 'crear':
            form = PerfilForm(request.POST, request.FILES)
        elif accion == 'actualizar':
            perfil = Perfil.objects.get(id=id)
            form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            perfil = form.save(commit=False)
            if accion == 'crear':  # Add this condition to assign the current user only when creating a new profile
                perfil.usuario = request.user
            perfil.save()
            form = PerfilForm(instance=perfil)
            messages.success(request, f'El perfil "{str(perfil.usuario.first_name)}" se logró {accion} correctamente')
            return redirect('admin_usuarios', 'actualizar', perfil.id)
        else:
            messages.error(request, f'No se pudo {accion} el perfil, pues el formulario no pasó las validaciones básicas')
            return redirect('admin_usuarios', 'actualizar', id)

    if request.method == 'GET':
        if accion == 'crear':
            form = PerfilForm()
        elif accion == 'actualizar':
            perfil = Perfil.objects.get(id=id)
            form = PerfilForm(instance=perfil)
        elif accion == 'eliminar':
            messages.success(request, eliminar_registro(Perfil, id))
            return redirect('admin_usuarios', accion='crear', id=0)

    perfiles = Perfil.objects.all()

    datos = {
        'form': form,
        'perfiles': perfiles
    }
    return render(request, 'admin_usuarios.html', datos)




def crear_perfil(request):
    form = RegistroAdminForm()
    if request.method == 'POST':
        form = RegistroAdminForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()  # Guardar el usuario para obtener un ID antes de asociar el perfil

            # Ahora `form.cleaned_data['imagen']` debería contener el objeto de archivo cargado
            perfil = Perfil(
                usuario=user,
                tipo_usuario=form.cleaned_data['tipo_usuario'],
                rut=form.cleaned_data['rut'],
                direccion=form.cleaned_data['direccion'],
                imagen=form.cleaned_data['imagen']  # Este es el objeto de archivo cargado
            )
            perfil.save()  # Guarda el perfil, que ahora incluye la imagen

            return redirect('admin_usuarios', 'crear', '0')
            
    return render(request, 'crear_perfil.html', {'form': form})


def generate_password(request):
    password = get_random_string(length=10)
    return JsonResponse({'password': password})



# Repite el patrón para médicos, secretarias, etc.

@login_required
def gestionar_agenda_medica(request):
    # Tu lógica aquí
    return render(request, 'gestionar_agenda_medica.html')

@login_required
def gestionar_horas_medicas(request):
    # Tu lógica aquí
    return render(request, 'gestionar_horas_medicas.html')

@login_required
def consultar_pacientes_en_espera(request):
    # Tu lógica aquí
    return render(request, 'consultar_pacientes_en_espera.html')

@login_required
def emitir_informes_transacciones(request):
    # Tu lógica aquí
    return render(request, 'emitir_informes_transacciones.html')

@login_required
def ingresar_pagos(request):
    # Tu lógica aquí
    return render(request, 'ingresar_pagos.html')

@login_required
def enviar_correos(request):
    # Tu lógica aquí
    return render(request, 'enviar_correos.html')


@login_required(login_url='ingresar')
def mis_datos(request):
    form = ActualizacionClienteForm(instance=request.user)
    perfil_form = PerfilForm(instance=request.user.perfil)
    password_form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        if 'perfil_form' in request.POST:
            perfil_form = PerfilFormParaMisDatos(request.POST, request.FILES, instance=request.user.perfil)  # Usar PerfilFormParaMisDatos en lugar de PerfilForm
            if perfil_form.is_valid():
                perfil = perfil_form.save(commit=False)
                perfil.tipo_usuario = request.user.perfil.tipo_usuario  # Establece el valor de tipo_usuario al original
                perfil.save()
                messages.success(request, 'Tu perfil ha sido actualizado.')
                return redirect('mis_datos')
        elif 'form' in request.POST:
            form = ActualizacionClienteForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Tu usuario ha sido actualizado.')
                return redirect('mis_datos')
        elif 'password_form' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Tu contraseña ha sido actualizada correctamente.')
                return redirect('mis_datos')

    rut = request.user.perfil.rut  # Obtén el valor del rut del usuario logueado
    direccion = request.user.perfil.direccion  # Obtén el valor de la dirección del usuario logueado
    imagen = request.user.perfil.imagen  # Obtén la imagen del usuario logueado

    return render(request, "mis_datos.html", {'form': form, 'perfil_form': perfil_form, 'password_form': password_form, 'user': request.user, 'rut': rut, 'direccion': direccion, 'imagen': imagen})


