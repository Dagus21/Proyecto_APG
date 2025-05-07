#-------------------------------------------------------------
#     Test: Gestión y Autenticación de Login
#-------------------------------------------------------------
"""
Autor: Carlos Andrés Jiménez Sarmiento (CJ)

Descripción:
Este test automatizado verifica el proceso de autenticación de usuario
a través de nick_name o email más contraseña.

Compatible con Pytest y Allure. Ejecutable también de forma manual.
"""

import pytest
import allure
from Gestion_y_Autenticacion_Login.GestionLogin import GestionLogin
from log import log_info, log_error, log_success

#-------------------------------------------------------------
#                  TEST DE LOGIN (PYTEST + MANUAL)
#-------------------------------------------------------------

@allure.feature("Login")
@allure.title("Autenticación de usuario con credenciales válidas")
def test_login_usuario():
    """
    Test de autenticación de usuario usando nick_name o email.
    """
    gestor = GestionLogin()
    credenciales = {
        "usuario": "Carlos_CJ",  # Puede ser nick_name o email
        "contrasena": "12345678"
    }

    try:
        resultado = gestor.login_usuario(credenciales)
        print(resultado)

        assert resultado["status"] == 200
        assert resultado["mensaje"] == "Acceso concedido."

        log_success("Test de login ejecutado correctamente.")
    except AssertionError:
        log_error("❌ El login no fue exitoso.")
        assert False
    except Exception as e:
        log_error(f"❌ Excepción en el test de login: {e}")
        assert False
    finally:
        log_info("Test de login finalizado.")

#-------------------------------------------------------------
#              EJECUCIÓN MANUAL (OPCIONAL)
#-------------------------------------------------------------
if __name__ == "__main__":
    try:
        test_login_usuario()
    except Exception as e:
        log_error(f"❌ Error al ejecutar manualmente: {e}")
