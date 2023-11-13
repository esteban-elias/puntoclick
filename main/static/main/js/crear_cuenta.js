document.addEventListener('DOMContentLoaded', () => {
    const btnCrearCuenta = document.getElementById('btn-crear-cuenta');
    const error = document.getElementById('error');
    
    btnCrearCuenta.addEventListener('click', function () {
        if (document.getElementById('contrasena').value
            !== document.getElementById('confirmar-contrasena').value) {
            error.innerHTML = 'Las contraseñas no coinciden';
            return;
        }
        const form = this.closest('form');
        const url = form.action;
        const formData = new FormData(form);
        
        axios
        .post(url, formData)
        .then((response) => {
            console.log(response);
            if (response.data.status === 'success') {
                window.location.href = '/';
            } else {
                error.innerHTML = response.data.message;
            }
        })
        .catch((error) => {
            console.log(error);
        });
    });
    }
);
