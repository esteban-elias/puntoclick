from django.shortcuts import render
from .models import Categoria


def index(request):
    categorias = Categoria.objects.all()
    context = {
        'categorias': categorias
    }
    return render(request, 'index.html', context)
