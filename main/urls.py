from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categorias/<int:id_categoria>', views.categoria, name='categoria'),
    path('producto/<int:id_producto>', views.producto, name='producto'),
    path('carrito', views.carrito, name='carrito'),

    path('agregar-al-carrito/<int:id_producto>', views.agregar_al_carrito,
         name='agregar_al_carrito'),
    path('incrementar-item-carrito/<int:id_item>',
         views.incrementar_item_carrito,
         name='incrementar_item_carrito'),
    path('decrementar-item-carrito/<int:id_item>',
         views.decrementar_item_carrito,
         name='decrementar_item_carrito'),
    path('eliminar-item-carrito/<int:id_item>',
         views.eliminar_item_carrito,
         name='eliminar_item_carrito'),
    path('iniciar-sesion', views.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar-sesion', views.cerrar_sesion, name='cerrar_sesion'),
    path('cuenta', views.cuenta, name='cuenta'),
    path('crear-cuenta', views.crear_cuenta, name='crear_cuenta'),
]
