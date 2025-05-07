function togglePassword(button) {
    const input = document.getElementById('input-contrasena');
    const showing = input.type === 'text';
    input.type = showing ? 'password' : 'text';
    button.innerText = showing ? '👁️' : '🙈';
  }
  