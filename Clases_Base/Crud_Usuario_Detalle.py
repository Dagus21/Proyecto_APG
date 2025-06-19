#-------------------------------------------------------------
#                  Librerías e Importaciones
#-------------------------------------------------------------
"""
Archivo: Crud_Usuario_Detalle.py

Implementa operaciones CRUD completas para las tablas `usuarios` y `detalle_usuarios`,
relacionadas mediante `id_usuario`. Este CRUD hereda de `Conexiona_Data_Base`.

Características:
- Crea el usuario y su detalle (ambos registros).
- Lee todos los usuarios o uno por ID.
- Actualiza campos en ambas tablas.
- Elimina en cascada ambos registros.
- Registra logs estructurados y devuelve respuestas formateadas.

Autor: Carlos Andrés Jiménez Sarmiento (CJ)
"""

from datetime import date

import psycopg2
from Clases_Base.Conexion_Data_Base import Conexion_Data_Base
from log import log_info, log_error, log_success, log_warning
from datetime import date 
import bcrypt

class CrudUsuarioDetalle(Conexion_Data_Base):

#-------------------------------------------------------------
#            CRUD: Usuario y Detalle
#-------------------------------------------------------------

    def crear_usuario_con_detalle(self, data):
        """
        Crea un nuevo usuario y su detalle asociado en la base de datos.

        Args:
            data (dict): Diccionario con las claves:
                - nombre (str)
                - nick_name (str)
                - contrasena (str)
                - email (str)

        Returns:
            dict: Respuesta estructurada con status, mensaje y data.
        """
        try:
            self.conectar()

            log_info("Iniciando inserción de nuevo usuario y detalle...")

            # Obtener fecha actual
            fecha_actual = date.today()
            
            # Hashear la contraseña (opcional, si se requiere)
            contrasena_hash = self.generar_hash_contrasena(data['contrasena'])
            
            # Grupo por defecto (1) y estado de cuenta (False)
            grupo = 1 
            estado_cuenta = False

            # Insertar en tabla usuarios
            self.cursor.execute("""
                INSERT INTO usuarios (nombre, nick_name, fecha)
                VALUES (%s, %s, %s)
                RETURNING id_usuario;
            """, (data['nombre'], data['nick_name'], fecha_actual))

            id_usuario = self.cursor.fetchone()[0]
            log_info(f"Usuario creado con ID: {id_usuario}")

            # Insertar en tabla detalle_usuarios
            self.cursor.execute("""
                INSERT INTO detalle_usuarios (
                    id_usuario, contrasena, token, grupo, email, estado_cuenta)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                id_usuario,
                contrasena_hash,
                '',                  # token vacío por defecto
                grupo,           # grupo por defecto
                data['email'],
                estado_cuenta               # estado_cuenta por defecto
            ))

            self.conn.commit()
            log_success("Usuario y detalle insertados correctamente.")

            return {
                "status": 201,
                "mensaje": "Usuario creado exitosamente.",
                "data": {"id_usuario": id_usuario}
            }

        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            log_error(f"Violación de integridad: {str(e)}")
            return {
                "status": 400,
                "mensaje": f"Error: violación de restricción de integridad (unicidad o clave foránea).",
                "data": None
            }

        except Exception as e:
            self.conn.rollback()
            log_error(f"Error general al crear usuario: {str(e)}")
            return {
                "status": 500,
                "mensaje": "Error interno al crear usuario.",
                "data": None
            }

        finally:
            self.cerrar_conexion()
            log_info("Transacción de creación de usuario finalizada.")
            
    def leer_usuarios_con_detalle(self):
        """
        Recupera todos los usuarios junto con su detalle correspondiente.

        Returns:
            dict: Respuesta estructurada con status, mensaje y data (lista de usuarios con detalles).
        """
        try:
            self.conectar()
            log_info("Iniciando lectura de usuarios y sus detalles...")

            self.cursor.execute("""
                SELECT u.id_usuario, u.nombre, u.nick_name, u.fecha,
                    d.id_detalle_usuarios, d.contrasena, d.token,
                    d.grupo, d.email, d.estado_cuenta
                FROM usuarios u
                JOIN detalle_usuarios d ON u.id_usuario = d.id_usuario;
            """)
            filas = self.cursor.fetchall()

            columnas = [desc[0] for desc in self.cursor.description]
            data = [dict(zip(columnas, fila)) for fila in filas]

            log_success(f"Se recuperaron {len(data)} registros de usuarios con detalles.")

            return {
                "status": 200,
                "mensaje": "Usuarios recuperados correctamente.",
                "data": data
            }

        except Exception as e:
            log_error(f"❌ Error al leer usuarios con detalles: {str(e)}")
            return {
                "status": 500,
                "mensaje": "Error interno al recuperar los usuarios.",
                "data": None
            }

        finally:
            self.cerrar_conexion()
            log_info("Lectura de usuarios con detalles finalizada.")

    def leer_por_usuario(self, id_usuario):
        """
        Obtiene los datos del usuario y su detalle correspondiente.

        Acepta como parámetro el ID del usuario, el nick_name o el email.

        Args:
            id_usuario (Union[int, str]): ID, nick_name o email del usuario a consultar.

        Returns:
            dict: Respuesta estructurada con status, mensaje y data.
        """
        try:
            self.conectar()

            # Detectar tipo de criterio
            if isinstance(id_usuario, int):
                campo = "u.id_usuario"
            elif "@" in str(id_usuario):
                campo = "d.email"
            else:
                campo = "u.nick_name"

            log_info(f"Iniciando búsqueda del usuario por '{campo}' = '{id_usuario}'...")

            # Consulta unificada
            self.cursor.execute(f"""
                SELECT u.id_usuario, u.nombre, u.nick_name, u.fecha,
                    d.contrasena, d.token, d.grupo, d.email, d.estado_cuenta
                FROM usuarios u
                JOIN detalle_usuarios d ON u.id_usuario = d.id_usuario
                WHERE {campo} = %s;
            """, (id_usuario,))

            fila = self.cursor.fetchone()

            if not fila:
                log_warning(f"No se encontró usuario con el id_usuario '{id_usuario}'.")
                return {
                    "status": 404,
                    "mensaje": "Usuario no encontrado.",
                    "data": None
                }

            resultado = {
                "id_usuario": fila[0],
                "nombre": fila[1],
                "nick_name": fila[2],
                "fecha": str(fila[3]),
                "contrasena": fila[4],
                "token": fila[5],
                "grupo": fila[6],
                "email": fila[7],
                "estado_cuenta": fila[8]
            }

            log_success(f"Consulta completada para el id_usuario '{id_usuario}'.")
            return {
                "status": 200,
                "mensaje": "Datos obtenidos correctamente.",
                "data": resultado
            }

        except Exception as e:
            log_error(f"Error al consultar usuario: {str(e)}")
            return {
                "status": 500,
                "mensaje": "Error interno al consultar usuario.",
                "data": None
            }

        finally:
            self.cerrar_conexion()
            log_info("Finalización de consulta de usuario.")

    def actualizar_usuario_con_detalle(self, id_usuario, data):
        """
        Actualiza los datos del usuario y su detalle con base en un id_usuario flexible.

        Args:
            id_usuario (Union[int, str]): puede ser ID, nick_name o email.
            data (dict): Campos a actualizar opcionales:
                - nombre (str)
                - nick_name (str)
                - fecha (str)
                - contrasena (str)
                - grupo (int)
                - email (str)
                - estado_cuenta (bool)

        Returns:
            dict: Respuesta con status, mensaje y data.
        """
        try:
            self.conectar()

            # Detectar tipo de búsqueda
            if isinstance(id_usuario, int):
                campo = "u.id_usuario"
            elif "@" in str(id_usuario):
                campo = "d.email"
            else:
                campo = "u.nick_name"

            log_info(f"Iniciando actualización del usuario por '{campo}' = '{id_usuario}'...")

            # Obtener ID real del usuario
            self.cursor.execute(f"""
                SELECT u.id_usuario
                FROM usuarios u
                JOIN detalle_usuarios d ON u.id_usuario = d.id_usuario
                WHERE {campo} = %s;
            """, (id_usuario,))
            resultado = self.cursor.fetchone()

            if not resultado:
                log_warning(f"No se encontró usuario con el id_usuario '{id_usuario}'.")
                return {
                    "status": 404,
                    "mensaje": "Usuario no encontrado.",
                    "data": None
                }

            id_usuario_real = resultado[0]

            # Actualizar tabla usuarios
            if any(k in data for k in ('nombre', 'nick_name', 'fecha')):
                campos_usuario = []
                valores_usuario = []

                if 'nombre' in data:
                    campos_usuario.append("nombre = %s")
                    valores_usuario.append(data['nombre'])

                if 'nick_name' in data:
                    campos_usuario.append("nick_name = %s")
                    valores_usuario.append(data['nick_name'])

                if 'fecha' in data:
                    campos_usuario.append("fecha = %s")
                    valores_usuario.append(data['fecha'])

                valores_usuario.append(id_usuario_real)

                self.cursor.execute(f"""
                    UPDATE usuarios
                    SET {', '.join(campos_usuario)}
                    WHERE id_usuario = %s;
                """, tuple(valores_usuario))
                log_info("Tabla 'usuarios' actualizada.")


            # Actualizar tabla detalle_usuarios
            if any(k in data for k in ('contrasena', 'grupo', 'email', 'estado_cuenta')):
                campos_detalle = []
                valores_detalle = []

                if 'contrasena' in data:
                    campos_detalle.append("contrasena = %s")
                    valores_detalle.append(self.generar_hash_contrasena(data['contrasena']))

                if 'grupo' in data:
                    campos_detalle.append("grupo = %s")
                    valores_detalle.append(data['grupo'])

                if 'email' in data:
                    campos_detalle.append("email = %s")
                    valores_detalle.append(data['email'])

                if 'estado_cuenta' in data:
                    campos_detalle.append("estado_cuenta = %s")
                    valores_detalle.append(data['estado_cuenta'])

                valores_detalle.append(id_usuario_real)

                self.cursor.execute(f"""
                    UPDATE detalle_usuarios
                    SET {', '.join(campos_detalle)}
                    WHERE id_usuario = %s;
                """, tuple(valores_detalle))
                log_info("Tabla 'detalle_usuarios' actualizada.")

            self.conn.commit()
            log_success(f"Usuario actualizado correctamente con ID {id_usuario_real}.")

            return {
                "status": 200,
                "mensaje": "Usuario actualizado exitosamente.",
                "data": {"id_usuario": id_usuario_real}
            }

        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            log_error(f"Violación de integridad al actualizar: {str(e)}")
            return {
                "status": 400,
                "mensaje": "Violación de restricción de integridad (unicidad, claves).",
                "data": None
            }

        except Exception as e:
            self.conn.rollback()
            log_error(f"Error general al actualizar usuario: {str(e)}")
            return {
                "status": 500,
                "mensaje": "Error interno al actualizar usuario.",
                "data": None
            }

        finally:
            self.cerrar_conexion()
            log_info("Transacción de actualización finalizada.")

            self.cerrar_conexion()
            log_info("Transacción de eliminación finalizada.")

    def eliminar_usuario_con_detalle(self, id_usuario):
        """
        Elimina un usuario y su detalle asociado en base a un criterio flexible.

        Args:
            id_usuario (Union[int, str]): Puede ser ID, nick_name o email.

        Returns:
            dict: Respuesta estructurada con status, mensaje y data.
        """
        try:
            self.conectar()

            # Detectar tipo de criterio
            if isinstance(id_usuario, int):
                campo = "u.id_usuario"
            elif "@" in str(id_usuario):
                campo = "d.email"
            else:
                campo = "u.nick_name"

            log_info(f"Iniciando eliminación del usuario por '{campo}' = '{id_usuario}'...")

            # Obtener ID real del usuario
            self.cursor.execute(f"""
                SELECT u.id_usuario
                FROM usuarios u
                JOIN detalle_usuarios d ON u.id_usuario = d.id_usuario
                WHERE {campo} = %s;
            """, (id_usuario,))
            resultado = self.cursor.fetchone()

            if not resultado:
                log_warning(f"No se encontró usuario con el criterio '{id_usuario}'.")
                return {
                    "status": 404,
                    "mensaje": "Usuario no encontrado.",
                    "data": None
                }

            id_usuario_real = resultado[0]

            # Eliminar primero el detalle
            self.cursor.execute("DELETE FROM detalle_usuarios WHERE id_usuario = %s;", (id_usuario_real,))
            log_info("Detalle del usuario eliminado.")

            # Eliminar el usuario
            self.cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s;", (id_usuario_real,))
            self.conn.commit()

            log_success(f"Usuario con ID {id_usuario_real} eliminado correctamente.")

            return {
                "status": 200,
                "mensaje": "Usuario eliminado exitosamente.",
                "data": {"id_usuario": id_usuario_real}
            }

        except Exception as e:
            self.conn.rollback()
            log_error(f"Error al eliminar usuario: {str(e)}")
            return {
                "status": 500,
                "mensaje": "Error interno al eliminar usuario.",
                "data": None
            }

        finally:
            self.cerrar_conexion()
            log_info("Transacción de eliminación finalizada.")

    def eliminar_usuarios_no_verificados_expirados(self):
        """
        Elimina usuarios que no han verificado su cuenta después de 72 horas desde la creación.

        Returns:
            dict: Respuesta estructurada con status, mensaje y data (cantidad eliminada).
        """
        try:
            self.conectar()
            log_info("Iniciando eliminación de cuentas no verificadas con más de 72 horas...")

            # Calcular fecha límite (72 horas atrás)
            from datetime import timedelta, datetime
            limite = datetime.now().date() - timedelta(days=3)

            # 1. Obtener IDs de usuarios no verificados y creados hace más de 72 horas
            self.cursor.execute("""
                SELECT u.id_usuario
                FROM usuarios u
                JOIN detalle_usuarios d ON u.id_usuario = d.id_usuario
                WHERE d.estado_cuenta = FALSE
                  AND u.fecha <= %s;
            """, (limite, ))
            ids_a_eliminar = [row[0] for row in self.cursor.fetchall()]

            if not ids_a_eliminar:
                log_info("No hay cuentas no verificadas para eliminar.")
                return {
                    "status": 200,
                    "mensaje": "No hay cuentas expiradas por eliminar.",
                    "data": {"cantidad_eliminada": 0}
                }

            # 2. Eliminar en cascada cada usuario
            cantidad = 0
            for id_usuario in ids_a_eliminar:
                self.cursor.execute("DELETE FROM detalle_usuarios WHERE id_usuario = %s;", (id_usuario,))
                self.cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s;", (id_usuario,))
                cantidad += 1

            self.conn.commit()
            log_success(f"Se eliminaron {cantidad} usuarios no verificados con más de 72 horas.")

            return {
                "status": 200,
                "mensaje": f"Eliminados {cantidad} usuarios no verificados y expirados.",
                "data": {"cantidad_eliminada": cantidad}
            }

        except Exception as e:
            self.conn.rollback()
            log_error(f"Error al eliminar cuentas expiradas: {str(e)}")
            return {
                "status": 500,
                "mensaje": "Error al eliminar cuentas expiradas.",
                "data": None
            }
        finally:
            self.cerrar_conexion()
            log_info("Transacción de limpieza de usuarios expirados finalizada.")

#-------------------------------------------------------------
#                  Funciones Auxiliares
#-------------------------------------------------------------
    @staticmethod
    def generar_hash_contrasena(contrasena_plana: str) -> str:
        """
        Genera un hash seguro de una contraseña utilizando bcrypt.

        Args:
            contrasena_plana (str): Contraseña sin cifrar proporcionada por el usuario.

        Returns:
            str: Hash de la contraseña codificado en UTF-8.
        """
        salt = bcrypt.gensalt(rounds=12)  # Nivel de seguridad (cost factor) = 12
        hash_bytes = bcrypt.hashpw(contrasena_plana.encode('utf-8'), salt)
        return hash_bytes.decode('utf-8')
