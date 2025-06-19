function togglePassword(button, id) {
  const input = document.getElementById(id);
  const isVisible = input.type === "text";
  input.type = isVisible ? "password" : "text";
  button.innerText = isVisible ? "👁️" : "🙈";
}

// --- Validación en tiempo real ---

const requisitos = [
  { regex: /^.{8,16}$/, id: "req-len" },
  { regex: /^[^\s]+$/, id: "req-nocontrol" },
  { regex: /[A-Z]/, id: "req-upper" },
  { regex: /[0-9]/, id: "req-num" },
  { regex: /[^A-Za-z0-9]/, id: "req-special" }
];

function validarRequisitos(password) {
  let valido = true;
  requisitos.forEach(req => {
    const elem = document.getElementById(req.id);
    if (req.regex.test(password)) {
      elem.classList.add("ok");
    } else {
      elem.classList.remove("ok");
      valido = false;
    }
  });
  return valido;
}

const contrasenaInput = document.getElementById("contrasena");
const confirmarInput = document.getElementById("confirmar");
const coincidenciaMsg = document.getElementById("coincidencia-msg");
const btnRegistrar = document.getElementById("btn-registrar");

function verificarCoincidencia() {
  if (!contrasenaInput.value && !confirmarInput.value) {
    coincidenciaMsg.innerText = "";
    coincidenciaMsg.classList.remove("ok");
    return false;
  }
  if (contrasenaInput.value === confirmarInput.value) {
    coincidenciaMsg.innerText = "Las contraseñas coinciden ✔️";
    coincidenciaMsg.classList.add("ok");
    return true;
  } else {
    coincidenciaMsg.innerText = "Las contraseñas no coinciden";
    coincidenciaMsg.classList.remove("ok");
    return false;
  }
}

// Validación en tiempo real
contrasenaInput.addEventListener("input", function () {
  validarRequisitos(contrasenaInput.value);
  verificarCoincidencia();
  validarHabilitarBoton();
});
confirmarInput.addEventListener("input", function() {
  verificarCoincidencia();
  validarHabilitarBoton();
});

// Bloquea o habilita el botón de registrar
function validarHabilitarBoton() {
  if (
    validarRequisitos(contrasenaInput.value) &&
    verificarCoincidencia()
  ) {
    btnRegistrar.disabled = false;
  } else {
    btnRegistrar.disabled = true;
  }
}

// --- Validación final y envío AJAX ---

document.getElementById("form-registro").addEventListener("submit", async function (e) {
  e.preventDefault();
  const form = e.target;
  const nombre = form.nombre.value.trim();
  const apellido = form.apellido.value.trim();
  const nick_name = form.nick_name.value.trim();
  const email = form.email.value.trim();
  const contrasena = contrasenaInput.value;
  const confirmar = confirmarInput.value;
  const msgError = document.getElementById("msg-error");
  msgError.classList.add("hidden");

  if (!nombre || !apellido) {
    msgError.innerText = "Nombre y Apellido son obligatorios.";
    msgError.classList.remove("hidden");
    form.nombre.focus();
    return;
  }
  // Email válido
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    msgError.innerText = "El correo electrónico no es válido.";
    msgError.classList.remove("hidden");
    form.email.focus();
    return;
  }
  // Contraseña cumple requisitos
  if (!validarRequisitos(contrasena)) {
    msgError.innerText = "La contraseña no cumple todos los requisitos.";
    msgError.classList.remove("hidden");
    contrasenaInput.focus();
    return;
  }
  // Contraseñas coinciden
  if (!verificarCoincidencia()) {
    msgError.innerText = "Las contraseñas no coinciden.";
    msgError.classList.remove("hidden");
    confirmarInput.focus();
    return;
  }

  // Desactiva botón mientras envía
  btnRegistrar.disabled = true;
  btnRegistrar.innerText = "Registrando...";

  // Datos a enviar
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
      btnRegistrar.disabled = false;
      btnRegistrar.innerText = "Registrarse";
    }
  } catch (err) {
    msgError.innerText = "Error en el servidor. Intenta más tarde.";
    msgError.classList.remove("hidden");
    btnRegistrar.disabled = false;
    btnRegistrar.innerText = "Registrarse";
  }
});

// Inicializa botón deshabilitado
window.addEventListener("DOMContentLoaded", () => {
  validarRequisitos(contrasenaInput.value);
  verificarCoincidencia();
  validarHabilitarBoton();
});
