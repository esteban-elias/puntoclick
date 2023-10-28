from django.contrib import admin
from .models import (Usuario, Direccion, Categoria, Producto, ImagenProducto, 
                     Pedido, DetallePedido, Pago, Resena, CarritoCompras, 
                     ItemCarrito, ListaDeseos, ItemListaDeseos)


admin.site.register(Usuario)
admin.site.register(Direccion)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(ImagenProducto)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Pago)
admin.site.register(Resena)
admin.site.register(CarritoCompras)
admin.site.register(ItemCarrito)
admin.site.register(ListaDeseos)
admin.site.register(ItemListaDeseos)
