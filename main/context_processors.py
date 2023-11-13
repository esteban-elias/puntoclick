from .models import Categoria, CarritoCompras, ItemCarrito

def categorias(request):
    categorias_padre = Categoria.objects.filter(categoria_padre__isnull=True)
    return {'categorias_padre': categorias_padre}


def carrito(request):
    if request.user.is_authenticated:
        carrito, _ = CarritoCompras.objects.get_or_create(usuario=request.user)
        items = ItemCarrito.objects.filter(carrito=carrito)
        ids_productos = [item.producto.id for item in items]
        return {
            'items_carrito': items,
            'ids_productos_carrito': ids_productos,
        }
    return {}
