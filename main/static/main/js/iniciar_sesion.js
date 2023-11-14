document.addEventListener('DOMContentLoaded', () => {
  const btnLogin = document.getElementById('btn-iniciar-sesion');

  btnLogin.addEventListener('click', function () {
    const form = this.closest('form');
    const url = form.action;
    const formData = new FormData(form);

    axios
      .post(url, formData)
      .then((response) => {
        console.log(response);
        if (response.data.status === 'success') {
          window.location.href =
            document.getElementById('next-url').value;
        } else {
          const error = document.getElementById('error');
          error.innerHTML = response.data.message;
        }
      })
      .catch((error) => {
        console.log(error);
      });
  });
});
