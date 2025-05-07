function cerrarSesion() {
    fetch("/login/cerrar", { method: "GET", credentials: "same-origin" })
      .then(() => {
        window.location.href = "/login/?mensaje=✅ Sesión cerrada correctamente.";
      })
      .catch((error) => {
        console.error("Error al cerrar sesión:", error);
        alert("Ocurrió un error al cerrar la sesión. Intenta de nuevo.");
      });
  }
  