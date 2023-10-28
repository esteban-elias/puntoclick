from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('categorias/<int:id_categoria>', views.categoria, name='categoria'),
]
