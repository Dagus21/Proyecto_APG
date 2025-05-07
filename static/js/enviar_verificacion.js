document.addEventListener("DOMContentLoaded", () => {
    const boton = document.getElementById("btn-verificar-cuenta");
  
    if (boton) {
      boton.addEventListener("click", async (e) => {
        e.preventDefault();
  
        try {
          const res = await fetch("/login/enviar-verificacion", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
          });
  
          const resultado = await res.json();
  
          if (resultado.status === 200) {
            alert("Correo de verificación enviado con éxito.");
          } else {
            alert(resultado.mensaje || "No se pudo enviar el correo.");
          }
        } catch (err) {
          alert("Error del servidor. Intenta de nuevo.");
        }
      });
    }
  });
  