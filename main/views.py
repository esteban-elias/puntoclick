from django.shortcuts import render
from .models import Categoria


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
