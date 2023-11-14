from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    pass

class Direccion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    direccion_calle = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=10)
    pais = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.direccion_calle}, {self.ciudad}, {self.estado}, {self.codigo_postal}, {self.pais}"


class Categoria(models.Model):
    nombre = models.CharField(max_length=255)
    categoria_padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_stock = models.PositiveIntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    url_imagen = models.URLField()
    es_primaria = models.BooleanField(default=False)

    def __str__(self):
        return self.url_imagen


class Pedido(models.Model):
    ESTADOS_CHOICES = [
        ('REALIZADO', 'Realizado'),
        ('ENVIADO', 'Enviado'),
        ('CANCELADO', 'Cancelado'),
        ('ENTREGADO', 'Entregado'),
    ]

    comprador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADOS_CHOICES,
                              default='REALIZADO')

    def __str__(self):
        return f"Pedido #{self.id} por {self.comprador}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_solicitada = models.PositiveIntegerField()
    precio_por_unidad = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"DetallePedido para Pedido #{self.pedido.id}"


class Pago(models.Model):
    METODOS_PAGO_CHOICES = [
        ('TARJETA_CREDITO', 'Tarjeta de Crédito'),
        ('PAYPAL', 'PayPal'),
    ]

    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO_CHOICES)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pago para Pedido #{self.pedido.id}"


class Resena(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    revisor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    calificacion = models.PositiveIntegerField()
    comentario = models.TextField()
    fecha_resena = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reseña por {self.revisor} para {self.producto.titulo}"


class CarritoCompras(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Carrito para {self.usuario}"


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(CarritoCompras, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"ItemCarrito para {self.carrito} - {self.producto.titulo}"

    @property
    def precio_total(self):
        return self.producto.precio * self.cantidad


class ListaDeseos(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Lista de deseos para {self.usuario}"


class ItemListaDeseos(models.Model):
    lista_deseos = models.ForeignKey(ListaDeseos, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return f"ItemListaDeseos para {self.producto.titulo}"

