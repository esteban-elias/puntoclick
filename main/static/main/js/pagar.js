document.addEventListener('DOMContentLoaded', function () {
  const direccion_calle = document.getElementById('id_direccion_calle');
  const ciudad = document.getElementById('id_ciudad');
  const estado = document.getElementById('id_estado');
  const codigo_postal = document.getElementById('id_codigo_postal');
  const pais = document.getElementById('id_pais');
  const metodo_pago = document.getElementById('id_metodo_pago');
  const btnPagar = document.getElementById('btn-pagar');

  btnPagar.addEventListener('click', function () {
    if (!validarCampos()) {
      return;
    }
    const data = new URLSearchParams();
    data.append('direccion-direccion_calle', direccion_calle.value);
    data.append('direccion-ciudad', ciudad.value);
    data.append('direccion-estado', estado.value);
    data.append('direccion-codigo_postal', codigo_postal.value);
    data.append('direccion-pais', pais.value);
    data.append('pago-metodo_pago', metodo_pago.value);

    axios
      .post(window.location.href, data)
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
});
