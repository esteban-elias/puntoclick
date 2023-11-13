from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from .models import Categoria, Producto, CarritoCompras, ItemCarrito, Usuario



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
    producto = Producto.objects.get(pk=id_producto)
    carrito, _ = CarritoCompras.objects.get_or_create(usuario=request.user)
    item, creado = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': 1}
    )
    if not creado:
        item.cantidad += 1
        item.save()
    return JsonResponse({
        'status': 'success',
        'message': 'Producto agregado al carrito'
    })


@require_POST
def incrementar_item_carrito(request, id_item):
    item = ItemCarrito.objects.get(pk=id_item)
    item.cantidad += 1
    item.save()
    return JsonResponse({
        'status': 'success',
        'message': 'Cantidad incrementada',
        'item' : item.to_dict() 
    })


@require_POST
def decrementar_item_carrito(request, id_item):
    item = ItemCarrito.objects.get(pk=id_item)
    if item.cantidad == 1:
        return HttpResponseBadRequest('No se puede decrementar')
    item.cantidad -= 1
    item.save()
    return JsonResponse({
        'status': 'success',
        'message': 'Cantidad decrementada',
        'item' : item.to_dict()
    })


@require_POST
def eliminar_item_carrito(request, id_item):
    item = ItemCarrito.objects.get(pk=id_item)
    item_copy = item.to_dict()
    item.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'Item eliminado',
        'item': item_copy
    })


def iniciar_sesion(request):
    if request.method == 'POST':
        nombre_usuario = request.POST['nombre-usuario']
        contrasena = request.POST['contrasena']
        usuario = authenticate(request, username=nombre_usuario, password=contrasena)
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
