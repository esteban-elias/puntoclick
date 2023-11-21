from copy import deepcopy
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import Categoria, Producto, Usuario, Pedido, Pago
from .forms import DireccionForm, PagoForm


def index(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()
    context = {
        'categorias': categorias,
        'productos': productos
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
    total_carrito = sum([item['precio'] * item['cantidad']
                        for item in carrito.values()])
    return JsonResponse({
        'status': 'success',
        'message': 'Cantidad incrementada',
        'item': carrito[id_producto],
        'total_carrito': total_carrito,
    })


@require_POST
def decrementar_item_carrito(request, id_producto):
    id_producto = str(id_producto)
    carrito = request.session.get('carrito', {})
    if carrito[id_producto]['cantidad'] == 1:
        return HttpResponseBadRequest('No se puede decrementar')
    carrito[id_producto]['cantidad'] -= 1
    request.session['carrito'] = carrito
    total_carrito = sum([item['precio'] * item['cantidad']
                        for item in carrito.values()])
    return JsonResponse({
        'status': 'success',
        'message': 'Cantidad decrementada',
        'item': carrito[id_producto],
        'total_carrito': total_carrito,
    })


@require_POST
def eliminar_item_carrito(request, id_producto):
    id_producto = str(id_producto)
    carrito = request.session.get('carrito', {})
    item_copy = deepcopy(carrito[id_producto])
    del carrito[id_producto]
    request.session['carrito'] = carrito
    total_carrito = sum([item['precio'] * item['cantidad']
                        for item in carrito.values()])
    return JsonResponse({
        'status': 'success',
        'message': 'Item eliminado',
        'item': item_copy,
        'total_carrito': total_carrito,
    })


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect('index')

    next_url = request.GET.get(
        'next') or request.META.get('HTTP_REFERER', '/')
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
    return render(request, 'iniciar_sesion.html', {'next_url': next_url})


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


def pagar(request):
    if not request.user.is_authenticated:
        return redirect(f'{reverse("iniciar_sesion")}?next=/pagar')

    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        monto = sum([item['precio'] * item['cantidad']
                    for item in carrito.values()])
        formDireccion = DireccionForm(request.POST, prefix='direccion')
        formPago = PagoForm(request.POST, prefix='pago')
        if formDireccion.is_valid() and formPago.is_valid():
            direccion = formDireccion.save(commit=False)
            direccion.usuario = request.user
            direccion.save()
            pedido = Pedido.objects.create(
                comprador=request.user,
                precio_total=monto,
                estado='REALIZADO'
            )
            pago = formPago.save(commit=False)
            pago.pedido = pedido
            pago.monto = monto
            pago.save()
            request.session['carrito'] = {}
            return JsonResponse({
                'status': 'success',
                'message': 'Pago realizado',
                'next_url': f'{reverse("boleta", args=[pago.id])}'
            })
        else:
            return HttpResponseBadRequest('No se pudo validar el formulario')
    context = {
        'direccion_form': DireccionForm(),
        'pago_form': PagoForm()
    }
    return render(request, 'pagar.html', context)


def boleta(request, id_pago):
    pago = get_object_or_404(Pago, pk=id_pago)
    if (not request.user.is_authenticated or
            request.user != pago.pedido.comprador):
        return HttpResponseForbidden('No tienes permiso para ver esta página')
    context = {
        'pago': pago
    }
    return render(request, 'boleta.html', context)
