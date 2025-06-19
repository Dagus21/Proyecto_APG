document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('reestablecerForm');
    const notificacion = document.getElementById('notificacion');
    const btnEnviar = document.getElementById('btnEnviar');

    let emailTemporal = null; // Para guardar el email temporalmente

    if (!form || !notificacion || !btnEnviar) {
        console.error('No se encontraron elementos necesarios');
        return;
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const email = form.email.value.trim();
        if (!validarEmail(email)) {
            mostrarNotificacion('Por favor, ingresa un correo electrónico válido.');
            return;
        }

        // Guardar el email antes de limpiar el campo
        emailTemporal = email;

        // Limpiar el campo del formulario
        form.reset();

        // Deshabilitar el botón mientras se procesa
        btnEnviar.disabled = true;
        btnEnviar.textContent = 'Enviando...';

        // Mostrar mensaje inmediato al usuario
        mostrarNotificacion(
            `Si estás registrado, se hará el envío del correo para restablecer contraseña${emailTemporal ? ` a <b>${emailTemporal}</b>` : ''}.`
        );

        // Tiempo mínimo de espera simulada (en ms)
        const MIN_ESPERA = 5000; // Puedes ajustar (1500-2000 recomendado)
        const start = Date.now();

        try {
            const formData = new FormData();
            formData.append('email', emailTemporal);

            const response = await fetch('/reestablecer/solicitar', {
                method: 'POST',
                body: formData
            });

            // Esperar el tiempo mínimo si la respuesta fue muy rápida
            const elapsed = Date.now() - start;
            if (elapsed < MIN_ESPERA) {
                await new Promise(r => setTimeout(r, MIN_ESPERA - elapsed));
            }

            // Procesa la respuesta del backend si necesitas manejar errores reales:
            if (!response.ok) {
                mostrarNotificacion('Hubo un problema al enviar el correo. Intenta de nuevo.');
            }
            // Si el backend te responde algo personalizado puedes procesarlo aquí (opcional).
        } catch (error) {
            mostrarNotificacion('Hubo un problema al enviar el correo.');
        } finally {
            btnEnviar.disabled = false;
            btnEnviar.textContent = 'Enviar enlace';
            emailTemporal = null; // Limpiar el temporal
        }
    });

    function mostrarNotificacion(mensaje) {
        notificacion.innerHTML = mensaje; // Permite etiquetas HTML (para poner el <b> en el correo)
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
