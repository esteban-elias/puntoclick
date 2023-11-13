document.addEventListener('DOMContentLoaded', () => {
  const btnsIncrementar = document.querySelectorAll('.btn-incrementar');
  const btnsDecrementar = document.querySelectorAll('.btn-decrementar');
  const btnsEliminar = document.querySelectorAll('.btn-eliminar');

  btnsIncrementar.forEach((btnIncrementar) => {
    const form = btnIncrementar.closest('form');
    const url = form.action;

    btnIncrementar.addEventListener('click', function () {
      const formData = new FormData(form);
      formData.append('action', 'incrementar');

      axios
        .post(url, formData)
        .then((response) => {
          console.log(response);
          if (response.data.status === 'success') {
            item = response.data.item;
            document.getElementById(`cantidad-${item.id}`).innerHTML =
              item.cantidad;
            document.getElementById(`total-${item.id}`).innerHTML =
              item.precio_total;
          }
        })
        .catch((error) => {
          console.log(error);
        });
    });
  });

  btnsDecrementar.forEach((btnDecrementar) => {
    const form = btnDecrementar.closest('form');
    const url = form.action;

    btnDecrementar.addEventListener('click', function () {
      const formData = new FormData(form);
      formData.append('action', 'decrementar');

      axios
        .post(url, formData)
        .then((response) => {
          console.log(response);
          if (response.data.status === 'success') {
            item = response.data.item;
            document.getElementById(`cantidad-${item.id}`).innerHTML =
              item.cantidad;
            document.getElementById(`total-${item.id}`).innerHTML =
              item.precio_total;
          }
        })
        .catch((error) => {
          console.log(error);
        });
    });
  });

  btnsEliminar.forEach((btnEliminar) => {
    const form = btnEliminar.closest('form');
    const url = form.action;

    btnEliminar.addEventListener('click', function () {
      const formData = new FormData(form);
      formData.append('action', 'eliminar');

      axios
        .post(url, formData)
        .then((response) => {
          console.log(response);
          if (response.data.status === 'success') {
            item = response.data.item;
            document.getElementById(`item-${item.id}`).remove();
          }
        })
        .catch((error) => {
          console.log(error);
        });
    });
  });
});
