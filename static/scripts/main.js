function mostrar(id) {
  document
    .querySelectorAll(".main")
    .forEach((div) => div.classList.remove("active"));
  document.getElementById(id).classList.add("active");
} 

function validarRegistro() {
  const inputs = document.querySelectorAll('#registro input');
  const correo = inputs[0].value.trim();
  const usuario = inputs[1].value.trim();
  const nombre = inputs[2].value.trim();
  const apellido = inputs[3].value.trim();
  const contrasena = inputs[4].value;

  const regexContrasena = /^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,16}$/;

  if (!correo || !usuario || !nombre || !apellido || !contrasena) {
    alert("Por favor, completa todos los campos.");
    return;
  }

  if (!regexContrasena.test(contrasena)) {
    alert("La contraseña debe tener entre 8 y 16 caracteres, al menos una mayúscula, un número y un carácter especial.");
    return;
  }

  // Enviar datos al backend Flask
  fetch('/registro', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ correo, usuario, nombre, apellido, contrasena })
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      mostrar('exito');
    } else {
      alert('Error al registrar');
    }
  })
  .catch(error => {
    console.error('Error en el registro:', error);
    alert('Ocurrió un error al registrar');
  });
}


function validarLogin() {
  const inputs = document.querySelectorAll('#login input');
  const usuario = inputs[0].value.trim();
  const contrasena = inputs[1].value;

  const regexContrasena = /^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,16}$/;

  if (!usuario || !contrasena) {
    alert("Ingresa tu usuario y contraseña.");
    return;
  }

  if (!regexContrasena.test(contrasena)) {
    alert("La contraseña que registraste tiene entre 8 y 16 caracteres, al menos una mayúscula, un número y un carácter especial.");
    return;
  }

  // Validar login con datos almacenados (si usas almacenamiento local, por ejemplo)
  mostrar('bienvenida');
}


//mostrar y ocultar contraseña
function togglePassword(inputId, btn) {
  const input = document.getElementById(inputId);
  const mostrarIcono = btn.dataset.show;
  const ocultarIcono = btn.dataset.hide;

  if (input.type === "password") {
    input.type = "text";
    btn.innerHTML = `<img src="${ocultarIcono}" alt="Ocultar contraseña" class="icono-ojo" />`;
  } else {
    input.type = "password";
    btn.innerHTML = `<img src="${mostrarIcono}" alt="Mostrar contraseña" class="icono-ojo" />`;
  }
}

