function togglePassword(button, id) {
    const input = document.getElementById(id);
    const isVisible = input.type === "text";
    input.type = isVisible ? "password" : "text";
    button.innerText = isVisible ? "👁️" : "🙈";
}

function validarContrasena(password) {
    const reglas = [
        { regex: /^.{8,16}$/, mensaje: "Debe tener entre 8 y 16 caracteres." },
        { regex: /^[^\s]+$/, mensaje: "No debe contener espacios." },
        { regex: /[A-Z]/, mensaje: "Debe incluir al menos una mayúscula." },
        { regex: /[0-9]/, mensaje: "Debe incluir al menos un número." },
        { regex: /[^A-Za-z0-9]/, mensaje: "Debe incluir al menos un carácter especial." }
    ];

    for (let r of reglas) {
        if (!r.regex.test(password)) {
            return r.mensaje;
        }
    }
    return null;
}

document.getElementById("form-cambiar-contrasena").addEventListener("submit", function (e) {
    const nueva = document.getElementById("nueva_contrasena").value;
    const confirmar = document.getElementById("confirmar_contrasena").value;
    const msgError = document.getElementById("msg-error");

    msgError.classList.add("hidden");
    msgError.innerText = ""; // Limpiar mensaje de error anterior

    const error = validarContrasena(nueva);
    if (error) {
        e.preventDefault();
        msgError.innerText = error;
        msgError.classList.remove("hidden");
        return;
    }

    if (nueva !== confirmar) {
        e.preventDefault();
        msgError.innerText = "Las contraseñas no coinciden.";
        msgError.classList.remove("hidden");
        return;
    }
});
