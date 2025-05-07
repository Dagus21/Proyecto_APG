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
  
  document.getElementById("form-cambiar").addEventListener("submit", function (e) {
    const actual = document.getElementById("actual").value;
    const nueva = document.getElementById("nueva").value;
    const confirmar = document.getElementById("confirmar").value;
    const msgError = document.getElementById("msg-error");
  
    // Solo limpiar mensaje si no venía del backend
    if (!msgError.innerText.trim()) {
      msgError.classList.add("hidden");
    }
  
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
  
    if (nueva === actual) {
      e.preventDefault();
      msgError.innerText = "La nueva contraseña no puede ser igual a la actual.";
      msgError.classList.remove("hidden");
      return;
    }
  });
  