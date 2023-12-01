document.addEventListener('DOMContentLoaded', function () {
  const direccion_calle = document.getElementById('id_direccion_calle');
  const ciudad = document.getElementById('id_ciudad');
  const estado = document.getElementById('id_estado');
  const codigo_postal = document.getElementById('id_codigo_postal');
  const pais = document.getElementById('id_pais');
  const metodo_pago = document.getElementById('id_metodo_pago');
  const btnPagar = document.getElementById('btn-pagar');
  const btnDescuento = document.getElementById('btn-descuento');
  const spanMonto = document.getElementById('span-monto');
  const montoSinDescuento = spanMonto.dataset.monto;

  const dataPagoForm = new URLSearchParams();

  btnDescuento.addEventListener('click', function () {
    const data = new URLSearchParams();
    form = btnDescuento.closest('form');
    const url = form.action;

    data.append(
      'codigo',
      document.getElementById('codigo_descuento').value
    );
    axios
      .post(url, data)
      .then((response) => {
        console.log(response);
        if (response.data.status === 'success') {
          alert('Descuento aplicado')
          spanMonto.textContent = toCLP((1 - response.data.descuento) * montoSinDescuento);
          dataPagoForm.append('descuento', response.data.descuento);
        } else {
          alert('Código inválido');
        }
      })
      .catch((error) => {
        console.log(error);
      });
  });

  btnPagar.addEventListener('click', function () {
    if (!validarCampos()) {
      return;
    }
    dataPagoForm.append('direccion-direccion_calle', direccion_calle.value);
    dataPagoForm.append('direccion-ciudad', ciudad.value);
    dataPagoForm.append('direccion-estado', estado.value);
    dataPagoForm.append('direccion-codigo_postal', codigo_postal.value);
    dataPagoForm.append('direccion-pais', pais.value);
    dataPagoForm.append('pago-metodo_pago', metodo_pago.value);

    axios
      .post(window.location.href, dataPagoForm)
      .then((response) => {
        console.log(response);
        if (response.data.status === 'success') {
          window.location.href = response.data.next_url;
        }
      })
      .catch((error) => {
        console.log(error);
      });
  });

  function validarCampos() {
    if (!direccion_calle.value) {
      alert('Por favor ingrese una dirección');
      return false;
    }
    if (!ciudad.value) {
      alert('Por favor ingrese una ciudad');
      return false;
    }
    if (!estado.value) {
      alert('Por favor ingrese un estado');
      return false;
    }
    if (!codigo_postal.value) {
      alert('Por favor ingrese un código postal');
      return false;
    }
    if (!pais.value) {
      alert('Por favor ingrese un país');
      return false;
    }
    if (!metodo_pago.value) {
      alert('Por favor ingrese un método de pago');
      return false;
    }
    return true;
  }
  
  function toCLP(value) {
    return new Intl.NumberFormat('es-CL', {
      style: 'currency',
      currency: 'CLP',
    }).format(value);
  }
});
