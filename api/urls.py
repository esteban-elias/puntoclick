from django.urls import path
from . import views

urlpatterns = [
  path('productos', views.productos),
  path('producto/<int:id_producto>', views.producto),
  path('crear_producto', views.crear_producto),
  path('modificar_producto/<int:id_producto>', views.modificar_producto),
  path('eliminar_producto/<int:id_producto>', views.eliminar_producto),
  path('pedidos', views.pedidos),
]

