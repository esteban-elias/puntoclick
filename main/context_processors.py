from .models import Categoria, Producto


def categorias(request):
    categorias_padre = Categoria.objects.filter(categoria_padre__isnull=True)
    return {'categorias_padre': categorias_padre}


def carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    for item in carrito.values():
        items.append({
            **item,
            'precio_total': item['precio'] * item['cantidad']
        })

    ids_productos = [item['id_producto'] for item in items]
    return {
        'items_carrito': items,
        'ids_productos_carrito': ids_productos,
    }
