from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from .models import Categoria, Producto, Usuario
from copy import deepcopy


def index(request):
    categorias = Categoria.objects.all()
    context = {
        'categorias': categorias
    }
    return render(request, 'index.html', context)


def categoria(request, id_categoria):
    categoria = Categoria.objects.get(pk=id_categoria)
    productos = categoria.producto_set.all()
    context = {
        'categoria': categoria,
        'productos': productos
    }
    return render(request, 'categoria.html', context)


def producto(request, id_producto):
    producto = Producto.objects.get(pk=id_producto)
    imagenes = producto.imagenproducto_set.all()
    context = {
        'producto': producto,
        'imagenes': imagenes
    }
    return render(request, 'producto.html', context)


def carrito(request):
    return render(request, 'carrito.html')


@require_POST
def agregar_al_carrito(request, id_producto):
    producto = get_object_or_404(Producto, pk=id_producto)
    carrito = request.session.get('carrito', {})
    carrito[producto.id] = {
        'id_producto': producto.id,
        'titulo': producto.titulo,
        'precio': int(producto.precio),
        'cantidad': 1
    }
    request.session['carrito'] = carrito
    return JsonResponse({
        'status': 'success',
        'message': 'Producto agregado al carrito'
    })


@require_POST
def incrementar_item_carrito(request, id_producto):
    id_producto = str(id_producto)
    carrito = request.session.get('carrito', {})
    carrito[id_producto]['cantidad'] += 1
    request.session['carrito'] = carrito
    return JsonResponse({
        'status': 'success',
        'message': 'Cantidad incrementada',
        'item': carrito[id_producto]
    })


@require_POST
def decrementar_item_carrito(request, id_producto):
    id_producto = str(id_producto)
    carrito = request.session.get('carrito', {})
    if carrito[id_producto]['cantidad'] == 1:
        return HttpResponseBadRequest('No se puede decrementar')
    carrito[id_producto]['cantidad'] -= 1
    request.session['carrito'] = carrito
    return JsonResponse({
        'status': 'success',
        'message': 'Cantidad decrementada',
        'item': carrito[id_producto]
    })


@require_POST
def eliminar_item_carrito(request, id_producto):
    id_producto = str(id_producto)
    carrito = request.session.get('carrito', {})
    item_copy = deepcopy(carrito[id_producto])
    del carrito[id_producto]
    request.session['carrito'] = carrito
    return JsonResponse({
        'status': 'success',
        'message': 'Item eliminado',
        'item': item_copy
    })


def iniciar_sesion(request):
    if request.method == 'POST':
        nombre_usuario = request.POST['nombre-usuario']
        contrasena = request.POST['contrasena']
        usuario = authenticate(
            request, username=nombre_usuario, password=contrasena)
        if usuario is not None:
            login(request, usuario)
            return JsonResponse({
                'status': 'success',
                'message': 'Usuario autenticado'
            })

        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Usuario o contraseña incorrectos'
            })
    return render(request, 'iniciar_sesion.html')


def cerrar_sesion(request):
    logout(request)
    return redirect('index')


def cuenta(request):
    usuario = request.user
    context = {
        'usuario': usuario
    }
    return render(request, 'cuenta.html', context)


def crear_cuenta(request):
    if request.method == 'POST':
        nombre_usuario = request.POST['nombre-usuario']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        email = request.POST['email']
        contrasena = request.POST['contrasena']
        usuario = Usuario.objects.create_user(
            username=nombre_usuario,
            first_name=nombre,
            last_name=apellido,
            email=email,
            password=contrasena
        )
        if usuario is not None:
            login(request, usuario)
            return JsonResponse({
                'status': 'success',
                'message': 'Usuario creado'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'No se pudo crear el usuario'
            })
    return render(request, 'crear_cuenta.html')
