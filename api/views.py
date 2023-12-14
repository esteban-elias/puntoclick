from rest_framework.response import Response
from rest_framework.decorators import api_view
from main.models import Producto, Pedido
from rest_framework import serializers


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'


@api_view(['GET'])
def productos(request):
    productos = Producto.objects.all()
    serializer_productos = ProductoSerializer(productos, many=True)
    data = {
        'productos': serializer_productos.data,
    }
    return Response(data)


@api_view(['GET'])
def producto(request, id_producto):
    producto = Producto.objects.get(pk=id_producto)
    serializer_producto = ProductoSerializer(producto)
    data = {
        'producto': serializer_producto.data,
    }
    return Response(data)


@api_view(['POST'])
def crear_producto(request):
    '''
    Ejemplo de request.data:
    {
      "titulo": "Carne Porotos",
      "descripcion": "Porotos",
      "precio": 7999.00,
      "cantidad_stock": "50",
      "vendedor": "2"
    }
    '''
    serializer_producto = ProductoSerializer(data=request.data)
    if serializer_producto.is_valid():
        serializer_producto.save()
        return Response(serializer_producto.data)
    else:
        return Response(serializer_producto.errors)


@api_view(['PUT'])
def modificar_producto(request, id_producto):
    producto = Producto.objects.get(pk=id_producto)
    serializer_producto = ProductoSerializer(producto, data=request.data)
    if serializer_producto.is_valid():
        serializer_producto.save()
        return Response(serializer_producto.data)
    else:
        return Response(serializer_producto.errors)


@api_view(['DELETE'])
def eliminar_producto(request, id_producto):
    producto = Producto.objects.get(pk=id_producto)
    producto.delete()
    return Response('Producto eliminado')


@api_view(['GET'])
def pedidos(request):
    pedidos = Pedido.objects.filter(comprador=request.user)
    serializer_pedidos = PedidoSerializer(pedidos, many=True)
    data = {
        'pedidos': serializer_pedidos.data,
    }
    return Response(data)
