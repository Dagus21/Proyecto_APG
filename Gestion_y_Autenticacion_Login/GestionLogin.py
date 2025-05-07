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
import bcrypt
import os
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_mail import Mail, Message
from flask import Flask
import os
from dotenv import load_dotenv
from flask import session


# Configuración única para Mail
load_dotenv()

app_mail = Flask(__name__)
app_mail.config['MAIL_SERVER'] = os.getenv("EMAIL_SERVER")
app_mail.config['MAIL_PORT'] = int(os.getenv("EMAIL_PORT"))
app_mail.config['MAIL_USE_TLS'] = True
app_mail.config['MAIL_USERNAME'] = os.getenv("EMAIL_USER")
app_mail.config['MAIL_PASSWORD'] = os.getenv("EMAIL_PASSWORD")

mail = Mail(app_mail)


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
                SELECT u.id_usuario, u.nick_name, d.contrasena, d.estado_cuenta, d.email
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

            id_usuario, nick_name, contrasena_hash, estado, email = usuario


            if not bcrypt.checkpw(contrasena_input.encode(), contrasena_hash.encode()):
                log_error("Contraseña incorrecta.")
                return {
                    "status": 401,
                    "mensaje": "Credenciales incorrectas.",
                    "data": None
                }
                
            
            log_success("Login exitoso.")
            session['id_usuario'] = id_usuario
            session['nick_name'] = nick_name
            session['estado_cuenta'] = estado
            session['autenticado'] = True
            session['email'] = email

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

    def cerrar_sesion(self):
        """
        Elimina todos los datos de sesión del usuario actual.
        """
        try:
            session.clear()
            log_success("Sesión cerrada correctamente.")
            return {"status": 200, "mensaje": "Sesión cerrada."}
        except Exception as e:
            log_error(f"Error al cerrar sesión: {str(e)}")
            return {"status": 500, "mensaje": "Error al cerrar sesión."}

    def verificar_sesion_activa(self):
        """
        Verifica si existe una sesión de usuario activa.
        """
        if session.get("autenticado"):
            return {
                "status": 200,
                "mensaje": "Sesión activa.",
                "data": {
                    "id_usuario": session.get("id_usuario"),
                    "nick_name": session.get("nick_name"),
                    "estado_cuenta": session.get("estado_cuenta")
                }
            }
        else:
            return {
                "status": 401,
                "mensaje": "No hay sesión activa.",
                "data": None
            }

    def enviar_correo_verificacion(self, correo: str, nick_name: str) -> dict:
        """
        Envía un correo con enlace de verificación de cuenta al correo proporcionado.

        Args:
            correo (str): Correo electrónico del usuario.
            nick_name (str): Nick del usuario para personalización del mensaje.

        Returns:
            dict: Diccionario estructurado con status, mensaje y token si aplica.
        """
        try:
            log_info(f"Iniciando generación de token para correo '{correo}'...")

            # Generación de token
            serializer = URLSafeTimedSerializer("clave_verificacion_basica")
            token = serializer.dumps(correo, salt="verificacion-cuenta")

            # Construcción del link de verificación
            dominio = os.getenv("FRONTEND_URL", "http://localhost:5000")
            link = f"{dominio}/login/verificar/{token}"
            log_info(f"Link generado: {link}")

            # Contenido HTML del correo
            cuerpo_html = f"""
            <html>
            <body>
                <h2>Hola {nick_name},</h2>
                <p>Gracias por registrarte. Para verificar tu cuenta, haz clic en el siguiente botón:</p>
                <p><a href="{link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none;">Verificar cuenta</a></p>
                <p>Este enlace estará activo por 1 hora.</p>
            </body>
            </html>
            """

            # Envío del correo
            mensaje = Message(
                subject="Verificación de cuenta",
                recipients=[correo],
                html=cuerpo_html,
                sender=os.getenv("EMAIL_USER")
            )
            with app_mail.app_context():
                mail.send(mensaje)


            log_success(f"Correo de verificación enviado correctamente a '{correo}'.")
            return {
                "status": 200,
                "mensaje": "Correo de verificación enviado.",
                "data": {"token": token}
            }

        except Exception as e:
            log_error(f"Error al enviar correo: {str(e)}")
            return {
                "status": 500,
                "mensaje": "Error al enviar el correo de verificación.",
                "data": None
            }

    def verificar_token(self, token: str) -> dict:
        """
        Valida el token de verificación de cuenta y actualiza estado_cuenta a True.

        Args:
            token (str): Token enviado al correo del usuario.

        Returns:
            dict: Respuesta con status, mensaje y resultado de la actualización.
        """
        try:
            log_info("Iniciando verificación de token...")

            # Deserializar y validar token (expira en 3600 segundos = 1 hora)
            serializer = URLSafeTimedSerializer("clave_verificacion_basica")
            correo = serializer.loads(token, salt="verificacion-cuenta", max_age=3600)

            log_info(f"Token válido para correo '{correo}'. Procediendo a activar cuenta...")

            # Reutilizar función de actualización del CRUD base
            resultado = self.actualizar_usuario_con_detalle(correo, {"estado_cuenta": True})

            if resultado["status"] == 200:
                log_success("Cuenta verificada exitosamente.")
                return {
                    "status": 200,
                    "mensaje": "Cuenta verificada correctamente.",
                    "data": resultado["data"]
                }
            else:
                log_error("Error al actualizar estado de cuenta.")
                return {
                    "status": 500,
                    "mensaje": "No se pudo verificar la cuenta.",
                    "data": resultado["data"]
                }

        except SignatureExpired:
            log_error("Token expirado.")
            return {
                "status": 400,
                "mensaje": "El enlace ha expirado. Solicita uno nuevo.",
                "data": None
            }

        except BadSignature:
            log_error("Token inválido.")
            return {
                "status": 400,
                "mensaje": "El enlace de verificación no es válido.",
                "data": None
            }

        except Exception as e:
            log_error(f"Error durante verificación de token: {str(e)}")
            return {
                "status": 500,
                "mensaje": "Error interno al verificar cuenta.",
                "data": None
            }
