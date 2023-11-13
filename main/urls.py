from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('categorias/<int:id_categoria>', views.categoria, name='categoria'),
  path('producto/<int:id_producto>', views.producto, name='producto'),
  path('carrito', views.carrito, name='carrito'),

  path('agregar-al-carrito/<int:id_producto>', views.agregar_al_carrito, 
       name='agregar_al_carrito'),
  path('actualizar-carrito/<int:id_item>', views.actualizar_carrito,
       name='actualizar_carrito'),
]
