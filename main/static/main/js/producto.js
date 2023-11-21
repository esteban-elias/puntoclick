document.addEventListener('DOMContentLoaded', () => {
  const btnAgregarAlCarrito = document.getElementById(
    'btn-agregar-al-carrito'
  );

  btnAgregarAlCarrito.addEventListener('click', function () {
    const form = this.closest('form');
    const url = form.action;

    axios
      .post(url)
      .then((response) => {
        console.log(response);
        if (response.data.status === 'success') {
          form.innerHTML = `<li class="list-group-item">Producto añadido al carrito</li>`;
        }
      })
      .catch((error) => {
        console.log(error);
      });
  });
});
