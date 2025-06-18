from Clases_Base.Crud_Usuario_Detalle import CrudUsuarioDetalle
from log import log_info, log_error, log_success
import secrets
import string
import os
from flask_mail import Message
from flask import current_app

class ReestablecerContrasena(CrudUsuarioDetalle):
    """
    Esta clase gestiona el proceso de recuperación de contraseñas.
    Permite la solicitud de un enlace de restablecimiento de contraseña mediante
    un token único que es enviado al correo electrónico del usuario.

    Hereda de `CrudUsuarioDetalle` para realizar las operaciones necesarias sobre la base de datos.
    """

    def solicitar_reestablecimiento(self, email):
        """
        Inicia el proceso de reestablecimiento de contraseña.
        Verifica si el email existe en la base de datos y genera un enlace con un token único 
        que será enviado al usuario.

        Args:
            email (str): El correo electrónico del usuario que solicita el reestablecimiento.

        Returns:
            dict: Un diccionario con el estado de la solicitud (status, mensaje, data).
                  Si el correo no existe, devuelve un mensaje de error.
                  Si el correo existe, genera un token y envía un enlace al usuario.
        """
        try:
            self.conectar()  # Establece la conexión con la base de datos
            log_info(f"Iniciando solicitud de reestablecimiento para email: {email}")

            # Verificar si el email existe en la base de datos
            self.cursor.execute(""" 
                SELECT u.id_usuario, d.email
                FROM usuarios u
                JOIN detalle_usuarios d ON u.id_usuario = d.id_usuario
                WHERE d.email = %s
            """, (email,))
            
            usuario = self.cursor.fetchone()
            
            if not usuario:
                return {
                    "status": 404,
                    "mensaje": "❌ No existe una cuenta con este correo electrónico."
                }
            
            # Generar un token único
            token = secrets.token_urlsafe(32)
            
            # Actualizar el token en la base de datos para este usuario
            self.cursor.execute(""" 
                UPDATE detalle_usuarios 
                SET token = %s
                WHERE email = %s
            """, (token, email))
            
            self.conn.commit()  # Guardar los cambios

            # Enviar el correo de reestablecimiento
            self._enviar_email_reestablecimiento(email, token)

            return {
                "status": 200,
                "mensaje": "✅ Se ha enviado un enlace a tu correo electrónico.",
                "data": {
                    "token": token,
                    "email": email
                }
            }
        
        except Exception as e:
            self.conn.rollback()  # Revertir cambios en caso de error
            log_error(f"Error en solicitar_reestablecimiento: {str(e)}")
            return {
                "status": 500,
                "mensaje": "❌ Error al procesar la solicitud."
            }

    def _enviar_email_reestablecimiento(self, email, token):
        """
        Envía un correo electrónico con el enlace de reestablecimiento de contraseña.
        El enlace incluye un token único que permite al usuario cambiar su contraseña.

        Args:
            email (str): El correo electrónico del destinatario.
            token (str): El token de reestablecimiento.

        Returns:
            None: El correo se envía al destinatario. Si ocurre algún error, se registra.
        """
        try:
            dominio = os.getenv("DIRECCION_URL", "http://localhost:5000")
            enlace = f"{dominio}/reestablecer/cambiar/{token}"
            sender = os.getenv("EMAIL_USER")  # Obtener el correo de la variable de entorno
            
            mensaje = Message(
                "Reestablecimiento de Contraseña",
                sender=sender,
                recipients=[email]
            )
            
            mensaje.html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #333; text-align: center;">Reestablecimiento de Contraseña</h2>
                
                <p style="color: #666; font-size: 16px;">Has solicitado reestablecer tu contraseña.</p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 0;">Para reestablecer tu contraseña, haz clic en el siguiente botón:</p>
                    <div style="text-align: center; margin-top: 20px;">
                        <a href="{enlace}" 
                           style="background-color: #007bff; color: white; padding: 12px 24px; 
                                  text-decoration: none; border-radius: 5px; display: inline-block;">
                            Reestablecer Contraseña
                        </a>
                    </div>
                </div>
                
                <p style="color: #666; font-size: 14px;">
                    <strong>Nota:</strong> Este enlace expirará en 24 horas.
                </p>
                
                <p style="color: #999; font-size: 12px; margin-top: 30px;">
                    Si no solicitaste este cambio, ignora este mensaje.
                </p>
            </div>
            """
            
            # Enviar el correo dentro del contexto de la aplicación
            with current_app.app_context():
                current_app.extensions['mail'].send(mensaje)

            log_success(f"Email de reestablecimiento enviado a {email}")
        except Exception as e:
            log_error(f"Error al enviar email de reestablecimiento: {str(e)}")
            raise

    def verificar_token(self, token):
        try:
            self.conectar()
            log_info(f"Verificando token recibido: {token}")
            self.cursor.execute("SELECT id_usuario FROM detalle_usuarios WHERE token = %s", (token,))
            resultado = self.cursor.fetchone()
            if not resultado:
                log_error(f"Token {token} no encontrado o inválido.")
                return {
                    "status": 400,
                    "mensaje": "❌ Token inválido."
                }
            log_info(f"Token válido para usuario: {resultado[0]}")
            return {
                "status": 200,
                "mensaje": "✅ Token válido."
            }
        except Exception as e:
            log_error(f"Error al verificar token: {str(e)}")
            return {
                "status": 500,
                "mensaje": "❌ Error al verificar el token."
            }




    def reestablecer_contrasena(self, token, nueva_contrasena):
        """
        Reestablece la contraseña de un usuario usando un token válido.
        Si el token es válido, actualiza la base de datos con la nueva contraseña.

        Args:
            token (str): El token de reestablecimiento de contraseña.
            nueva_contrasena (str): La nueva contraseña que el usuario desea establecer.

        Returns:
            dict: Un diccionario con el estado de la operación.
                Si el token es inválido, se retorna un mensaje de error.
                Si la contraseña es cambiada correctamente, se confirma el éxito de la operación.
        """
        try:
            self.conectar()  # Conectar a la base de datos
            log_info("Iniciando reestablecimiento de contraseña")

            # Verificar token y obtener el ID del usuario
            self.cursor.execute("""
                SELECT id_usuario
                FROM detalle_usuarios
                WHERE token = %s
            """, (token,))
            
            resultado = self.cursor.fetchone()
            
            if not resultado:
                log_error("Token no válido.")
                return {
                    "status": 400,
                    "mensaje": "❌ Token inválido."
                }

            id_usuario = resultado[0]

            # Generar el hash de la nueva contraseña
            contrasena_hash = self.generar_hash_contrasena(nueva_contrasena)

            # Actualizar la contraseña en la base de datos y limpiar el token
            self.cursor.execute("""
                UPDATE detalle_usuarios 
                SET contrasena = %s, token = NULL
                WHERE id_usuario = %s
            """, (contrasena_hash, id_usuario))
            
            self.conn.commit()  # Guardar los cambios

            log_success(f"Contraseña reestablecida para usuario {id_usuario}")
            return {
                "status": 200,
                "mensaje": "✅ Contraseña reestablecida exitosamente."
            }

        except Exception as e:
            self.conn.rollback()  # Revertir cambios en caso de error
            log_error(f"Error al reestablecer contraseña: {str(e)}")
            return {
                "status": 500,
                "mensaje": "❌ Error al reestablecer la contraseña."
            }


    def _generar_token(self):
        """
        Genera un token aleatorio seguro para reestablecer la contraseña.

        Returns:
            str: El token generado, que será enviado al usuario.
        """
        caracteres = string.ascii_letters + string.digits
        return ''.join(secrets.choice(caracteres) for _ in range(32))
