from django.shortcuts import render
from .models import Categoria, Producto


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
