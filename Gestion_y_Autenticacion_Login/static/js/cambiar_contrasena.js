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

const actualInput = document.getElementById("actual");
const nuevaInput = document.getElementById("nueva");
const confirmarInput = document.getElementById("confirmar");
const coincidenciaMsg = document.getElementById("coincidencia-msg");
const btnCambiar = document.getElementById("btn-cambiar");

function verificarCoincidencia() {
  if (!nuevaInput.value && !confirmarInput.value) {
    coincidenciaMsg.innerText = "";
    coincidenciaMsg.classList.remove("ok");
    return false;
  }
  if (nuevaInput.value === confirmarInput.value) {
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
nuevaInput.addEventListener("input", function () {
  validarRequisitos(nuevaInput.value);
  verificarCoincidencia();
  validarHabilitarBoton();
});
confirmarInput.addEventListener("input", function() {
  verificarCoincidencia();
  validarHabilitarBoton();
});
actualInput.addEventListener("input", validarHabilitarBoton);

// Bloquea o habilita el botón de cambiar
function validarHabilitarBoton() {
  if (
    validarRequisitos(nuevaInput.value) &&
    verificarCoincidencia() &&
    nuevaInput.value !== actualInput.value &&
    nuevaInput.value.length > 0 &&
    actualInput.value.length > 0
  ) {
    btnCambiar.disabled = false;
  } else {
    btnCambiar.disabled = true;
  }
}

// Validación final (en caso de que se fuerce el submit)
document.getElementById("form-cambiar").addEventListener("submit", function (e) {
  const actual = actualInput.value;
  const nueva = nuevaInput.value;
  const confirmar = confirmarInput.value;
  const msgError = document.getElementById("msg-error");

  // Solo limpiar mensaje si no venía del backend
  if (!msgError.innerText.trim()) {
    msgError.classList.add("hidden");
  }

  if (!validarRequisitos(nueva)) {
    e.preventDefault();
    msgError.innerText = "La nueva contraseña no cumple todos los requisitos.";
    msgError.classList.remove("hidden");
    nuevaInput.focus();
    return;
  }

  if (nueva !== confirmar) {
    e.preventDefault();
    msgError.innerText = "Las contraseñas no coinciden.";
    msgError.classList.remove("hidden");
    confirmarInput.focus();
    return;
  }

  if (nueva === actual) {
    e.preventDefault();
    msgError.innerText = "La nueva contraseña no puede ser igual a la actual.";
    msgError.classList.remove("hidden");
    nuevaInput.focus();
    return;
  }
});

// Inicializa feedback y botón deshabilitado al cargar
window.addEventListener("DOMContentLoaded", () => {
  validarRequisitos(nuevaInput.value);
  verificarCoincidencia();
  validarHabilitarBoton();
});
