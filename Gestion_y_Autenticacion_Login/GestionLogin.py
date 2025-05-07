#-------------------------------------------------------------
#     Clase: GestionLogin - Autenticación de Usuario
#-------------------------------------------------------------
"""
Este módulo permite autenticar usuarios mediante nick_name o email,
validando su contraseña con bcrypt. Hereda del CRUD base y utiliza
respuestas estructuradas y logs personalizados.

Ubicación: Gestion_y_Autenticacion_Login/GestionLogin.py
"""

from Clases_Base.Crud_Usuario_Detalle import CrudUsuarioDetalle
from log import log_info, log_error, log_success
import psycopg2
import bcrypt


class GestionLogin(CrudUsuarioDetalle):
    def login_usuario(self, credenciales):
        """
        Permite autenticar al usuario mediante nick_name o email + contraseña.

        Args:
            credenciales (dict): contiene 'usuario' (nick o email) y 'contrasena'.

        Returns:
            dict: respuesta con status, mensaje y data.
        """
        try:
            self.conectar()
            usuario_input = credenciales['usuario']
            contrasena_input = credenciales['contrasena']

            log_info("Verificando existencia de usuario...")

            self.cursor.execute("""
                SELECT u.id_usuario, u.nick_name, d.contrasena, d.estado_cuenta
                FROM usuarios u
                JOIN detalle_usuarios d ON u.id_usuario = d.id_usuario
                WHERE u.nick_name = %s OR d.email = %s;
            """, (usuario_input, usuario_input))

            usuario = self.cursor.fetchone()
            if not usuario:
                log_error("Usuario no encontrado.")
                return {
                    "status": 404,
                    "mensaje": "Usuario no registrado.",
                    "data": None
                }

            id_usuario, nick_name, contrasena_hash, estado = usuario

            if not bcrypt.checkpw(contrasena_input.encode(), contrasena_hash.encode()):
                log_error("Contraseña incorrecta.")
                return {
                    "status": 401,
                    "mensaje": "Credenciales incorrectas.",
                    "data": None
                }

            log_success("Login exitoso.")
            return {
                "status": 200,
                "mensaje": "Acceso concedido.",
                "data": {
                    "id_usuario": id_usuario,
                    "nick_name": nick_name,
                    "estado_cuenta": estado
                }
            }

        except Exception as e:
            log_error(f"Error en login: {str(e)}")
            return {
                "status": 500,
                "mensaje": "Error interno en el login.",
                "data": None
            }
        finally:
            self.cerrar_conexion()
            log_info("Proceso de login finalizado.")
