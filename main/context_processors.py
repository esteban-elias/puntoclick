from .models import Categoria

def categorias(request):
    categorias_padre = Categoria.objects.filter(categoria_padre__isnull=True)
    
    return {'categorias_padre': categorias_padre}
