#-------------------------------------------------------------
#     Test: Gestión y Autenticación de Login
#-------------------------------------------------------------
"""
Autor: Carlos Andrés Jiménez Sarmiento (CJ)

Descripción:
Este archivo contiene pruebas automatizadas para verificar el correcto
funcionamiento del sistema de autenticación y verificación de cuenta.
Incluye:
- Login de usuario
- Envío de correo de verificación
- Verificación de cuenta con token

Compatible con Pytest y Allure. También permite ejecución manual.
Ubicación: Gestion_y_Autenticacion_Login/test/main_test.py
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
    Test de autenticación de usuario usando nick_name o email más contraseña.
    """
    gestor = GestionLogin()
    credenciales = {
        "usuario": "Carlos_CJ",  # Puede ser nick_name o correo
        "contrasena": "12345678"
    }

    try:
        resultado = gestor.login_usuario(credenciales)
        print("Resultado login:", resultado)

        assert resultado["status"] == 200
        assert resultado["mensaje"] == "Acceso concedido."

        log_success("✅ Test de login ejecutado correctamente.")
    except AssertionError:
        log_error("❌ El login no fue exitoso.")
        assert False
    except Exception as e:
        log_error(f"❌ Excepción en el test de login: {e}")
        assert False
    finally:
        log_info("🧪 Test de login finalizado.")

#-------------------------------------------------------------
#       TEST DE ENVÍO DE CORREO DE VERIFICACIÓN
#-------------------------------------------------------------

@allure.feature("Correo de verificación")
@allure.title("Envío de correo con enlace de verificación")
def test_enviar_correo_verificacion():
    """
    Test de envío de correo de verificación al usuario con token incluido.
    """
    gestor = GestionLogin()
    correo = "carjisar@gmail.com"
    nick_name = "Carlos_CJ"

    try:
        resultado = gestor.enviar_correo_verificacion(correo, nick_name)
        print("Resultado envío:", resultado)

        assert resultado["status"] == 200
        assert resultado["mensaje"] == "Correo de verificación enviado."

        log_success("✅ Test de envío de correo ejecutado correctamente.")
    except AssertionError:
        log_error("❌ El envío de correo no fue exitoso.")
        assert False
    except Exception as e:
        log_error(f"❌ Excepción en el test de envío de correo: {e}")
        assert False
    finally:
        log_info("🧪 Test de envío de correo finalizado.")

#-------------------------------------------------------------
#         TEST DE VERIFICACIÓN DE CUENTA POR TOKEN
#-------------------------------------------------------------

@allure.feature("Verificación de Cuenta")
@allure.title("Verificación de cuenta con token válido")
def test_verificar_token():
    """
    Test completo que simula la verificación de cuenta con un token generado.
    """
    gestor = GestionLogin()
    correo = "carjisar@gmail.com"
    nick_name = "Carlos_CJ"

    try:
        # Paso 1: Generar el token con el correo y nick
        resultado_envio = gestor.enviar_correo_verificacion(correo, nick_name)
        print("Resultado envío:", resultado_envio)

        assert resultado_envio["status"] == 200
        token = resultado_envio["data"]["token"]

        # Paso 2: Verificar el token recibido (como si el usuario hiciera clic)
        resultado_verificacion = gestor.verificar_token(token)
        print("Resultado verificación:", resultado_verificacion)

        assert resultado_verificacion["status"] == 200
        assert resultado_verificacion["mensaje"] == "Cuenta verificada correctamente."

        log_success("✅ Test de verificación de cuenta ejecutado correctamente.")
    except AssertionError:
        log_error("❌ La verificación de cuenta no fue exitosa.")
        assert False
    except Exception as e:
        log_error(f"❌ Excepción en el test de verificación: {e}")
        assert False
    finally:
        log_info("🧪 Test de verificación de cuenta finalizado.")

#-------------------------------------------------------------
#              EJECUCIÓN MANUAL (OPCIONAL)
#-------------------------------------------------------------

if __name__ == "__main__":
    try:
        print("\n🔹 EJECUTANDO TEST DE LOGIN")
        test_login_usuario()

        print("\n🔹 EJECUTANDO TEST DE ENVÍO DE CORREO")
        test_enviar_correo_verificacion()

        print("\n🔹 EJECUTANDO TEST DE VERIFICACIÓN DE CUENTA")
        test_verificar_token()

    except Exception as e:
        log_error(f"❌ Error al ejecutar manualmente: {e}")
