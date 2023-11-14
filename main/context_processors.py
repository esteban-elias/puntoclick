from .models import Categoria, Producto


def categorias(request):
    categorias_padre = Categoria.objects.filter(categoria_padre__isnull=True)
    return {'categorias_padre': categorias_padre}


def carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    for item in carrito.values():
        producto = Producto.objects.get(pk=item['id_producto'])
        items.append({
            'producto': producto,
            'cantidad': item['cantidad'],
            'precio_total': producto.precio * item['cantidad']
        })

    ids_productos = [item['producto'].id for item in items]
    return {
        'items_carrito': items,
        'ids_productos_carrito': ids_productos,
    }
