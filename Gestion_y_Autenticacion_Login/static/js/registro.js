function togglePassword(button, id) {
    const input = document.getElementById(id);
    const isVisible = input.type === "text";
    input.type = isVisible ? "password" : "text";
    button.innerText = isVisible ? "👁️" : "🙈";
  }
  
  // Función para validar seguridad de contraseña
  function validarContrasena(password) {
    const requisitos = [
      { regex: /^.{8,16}$/, mensaje: "Debe tener entre 8 y 16 caracteres." },
      { regex: /^[^\s]+$/, mensaje: "No debe contener espacios." },
      { regex: /[A-Z]/, mensaje: "Debe incluir al menos una mayúscula." },
      { regex: /[0-9]/, mensaje: "Debe incluir al menos un número." },
      { regex: /[^A-Za-z0-9]/, mensaje: "Debe incluir al menos un carácter especial." }
    ];
  
    for (let regla of requisitos) {
      if (!regla.regex.test(password)) {
        return regla.mensaje;
      }
    }
    return null;
  }
  
  document.getElementById("form-registro").addEventListener("submit", async function (e) {
    e.preventDefault();
  
    const form = e.target;
    const nombre = form.nombre.value.trim();
    const apellido = form.apellido.value.trim();
    const segundo_nombre = form.segundo_nombre.value.trim();
    const segundo_apellido = form.segundo_apellido.value.trim();
    const nick_name = form.nick_name.value.trim();
    const email = form.email.value.trim();
    const contrasena = form.contrasena.value;
    const confirmar = form.confirmar.value;
    const msgError = document.getElementById("msg-error");
  
    msgError.classList.add("hidden");
  
    if (!nombre || !apellido) {
      msgError.innerText = "Nombre y Apellido son obligatorios.";
      msgError.classList.remove("hidden");
      return;
    }
  
    const errorValidacion = validarContrasena(contrasena);
    if (errorValidacion) {
      msgError.innerText = errorValidacion;
      msgError.classList.remove("hidden");
      return;
    }
  
    if (contrasena !== confirmar) {
      msgError.innerText = "Las contraseñas no coinciden.";
      msgError.classList.remove("hidden");
      return;
    }
  
    const data = {
      nombre: `${nombre} ${apellido}`,
      nick_name,
      email,
      contrasena
    };
  
    try {
      const res = await fetch("/login/registrar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
  
      const resultado = await res.json();
  
      if (resultado.status === 201) {
        window.location.replace("/login/");
      } else {
        msgError.innerText = resultado.mensaje || "Ocurrió un error.";
        msgError.classList.remove("hidden");
      }
  
    } catch (err) {
      msgError.innerText = "Error en el servidor. Intenta más tarde.";
      msgError.classList.remove("hidden");
    }
  });
  