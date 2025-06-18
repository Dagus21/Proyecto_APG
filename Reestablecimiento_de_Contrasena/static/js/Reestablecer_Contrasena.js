document.addEventListener('DOMContentLoaded', function() {
    console.log('Script cargado correctamente'); // Debug

    const form = document.getElementById('reestablecerForm');
    const notificacion = document.getElementById('notificacion');
    const btnEnviar = document.getElementById('btnEnviar');

    if (!form || !notificacion || !btnEnviar) {
        console.error('No se encontraron elementos necesarios');
        return;
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        console.log('Formulario enviado'); // Debug
        
        const email = form.email.value.trim();
        
        if (!validarEmail(email)) {
            mostrarNotificacion('Por favor, ingresa un correo electrónico válido.');
            return;
        }

        btnEnviar.disabled = true;
        btnEnviar.textContent = 'Enviando...';

        try {
            const formData = new FormData();
            formData.append('email', email);

            const response = await fetch('/reestablecer/solicitar', {
                method: 'POST',
                body: formData
            });

            mostrarNotificacion('Si estás registrado, se hará el envío del correo para restablecer contraseña.');
            form.reset();

        } catch (error) {
            console.error('Error:', error); // Debug
            mostrarNotificacion('Hubo un problema al enviar el correo.');
        } finally {
            btnEnviar.disabled = false;
            btnEnviar.textContent = 'Enviar enlace';
        }
    });

    function mostrarNotificacion(mensaje) {
        console.log('Mostrando notificación:', mensaje); // Debug
        
        notificacion.textContent = mensaje;
        notificacion.style.display = 'block';
        
        void notificacion.offsetHeight;
        
        notificacion.classList.add('mostrar');

        setTimeout(() => {
            notificacion.classList.remove('mostrar');
            setTimeout(() => {
                notificacion.style.display = 'none';
            }, 400);
        }, 5000);
    }

    function validarEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }
});
