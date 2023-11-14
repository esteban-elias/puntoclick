from django import forms
from .models import Direccion, Pago, Pedido

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['direccion_calle', 'ciudad', 'estado', 'codigo_postal', 'pais']


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['metodo_pago']
