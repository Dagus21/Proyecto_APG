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
  
  const nuevaInput = document.getElementById("nueva_contrasena");
  const confirmarInput = document.getElementById("confirmar_contrasena");
  const coincidenciaMsg = document.getElementById("coincidencia-msg");
  const btnRestablecer = document.getElementById("btn-restablecer");
  
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
  
  // Habilita o bloquea el botón
  function validarHabilitarBoton() {
    if (
      validarRequisitos(nuevaInput.value) &&
      verificarCoincidencia()
    ) {
      btnRestablecer.disabled = false;
    } else {
      btnRestablecer.disabled = true;
    }
  }
  
  // Validación final al submit (por si acaso)
  document.getElementById("form-cambiar-contrasena").addEventListener("submit", function (e) {
    const nueva = nuevaInput.value;
    const confirmar = confirmarInput.value;
    const msgError = document.getElementById("msg-error");
  
    msgError.classList.add("hidden");
    msgError.innerText = "";
  
    if (!validarRequisitos(nueva)) {
      e.preventDefault();
      msgError.innerText = "La contraseña no cumple todos los requisitos.";
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
  });
  
  // Inicializa feedback y botón deshabilitado al cargar
  window.addEventListener("DOMContentLoaded", () => {
    validarRequisitos(nuevaInput.value);
    verificarCoincidencia();
    validarHabilitarBoton();
  });
  