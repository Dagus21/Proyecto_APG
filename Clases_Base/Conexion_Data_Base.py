#-------------------------------------------------------------
#                    Librerías e Importaciones
#-------------------------------------------------------------
"""
Módulo base para conexión centralizada a base de datos PostgreSQL.

- psycopg2: Librería oficial para conectar con bases de datos PostgreSQL.
- log_info, log_error: Sistema de logging estructurado para trazabilidad.
"""

import psycopg2
from log import log_info, log_error

#-------------------------------------------------------------
#            Clase Base: Conexiona_Data_Base
#-------------------------------------------------------------
"""
Autor: Carlos Andrés Jiménez Sarmiento (CJ)

Descripción:
Clase encargada de establecer una conexión segura y reutilizable
a la base de datos PostgreSQL configurada en la nube (AWS RDS).

Cualquier funcionalidad que necesite acceso a la base de datos
puede heredar de esta clase y ejecutar sus consultas a través
del cursor compartido.

Características clave:
- Centralización de conexión.
- Reutilización mediante herencia.
- Manejo de errores con trazabilidad en logs.
- Compatible con pruebas automatizadas y Pytest.

Uso recomendado:
    class MiFuncionalidad(Conexiona_Data_Base):
        def __init__(self):
            super().__init__()
            self.conectar()

        def listar(self):
            self.cursor.execute("SELECT * FROM tabla")
            return self.cursor.fetchall()
"""

class Conexion_Data_Base_Nube:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def conectar(self):
        """
        Establece conexión con la base de datos PostgreSQL en la nube.

        Raises:
            Exception: Si ocurre un error durante la conexión.
        """
        try:
            self.conn = psycopg2.connect(
                host="hashing-bd.cw94q8sgiyyo.us-east-1.rds.amazonaws.com",
                user="grupo1",
                password="grupo1_123",
                dbname="postgres"  # Modifica si usas otro nombre de base de datos
            )
            self.cursor = self.conn.cursor()
            log_info("Conexión establecida exitosamente con la base de datos PostgreSQL.")
        except Exception as e:
            log_error(f"Error al conectar con PostgreSQL: {e}")
            raise

    def cerrar_conexion(self):
        """
        Cierra el cursor y la conexión si están activos.
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            log_info("Conexión con la base de datos cerrada correctamente.")
        except Exception as e:
            log_error(f"Error al cerrar la conexión: {e}")

#------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------
#                    Librerías e Importaciones
#-------------------------------------------------------------
"""
Módulo base para conexión centralizada a base de datos PostgreSQL local.

- psycopg2: Librería oficial para conectar con bases de datos PostgreSQL.
- log_info, log_error: Sistema de logging estructurado para trazabilidad.
"""

import psycopg2
from log import log_info, log_error

#-------------------------------------------------------------
#            Clase Base: Conexiona_Data_Base
#-------------------------------------------------------------
"""
Autor: Carlos Andrés Jiménez Sarmiento (CJ)

Descripción:
Clase encargada de establecer una conexión segura y reutilizable
a la base de datos PostgreSQL **local**.

Cualquier funcionalidad que necesite acceso a la base de datos
puede heredar de esta clase y ejecutar sus consultas a través
del cursor compartido.

Características clave:
- Centralización de conexión.
- Reutilización mediante herencia.
- Manejo de errores con trazabilidad en logs.
- Compatible con pruebas automatizadas y Pytest.
"""

class Conexion_Data_Base:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def conectar(self):
        """
        Establece conexión con la base de datos PostgreSQL local.

        Raises:
            Exception: Si ocurre un error durante la conexión.
        """
        try:
            self.conn = psycopg2.connect(
                host="localhost",           # Conexión local
                user="postgres",            # Usuario típico por defecto
                password="Cj_1006744921",   # Tu contraseña
                dbname="DB_APG_CJ",         # Tu base de datos
                port=5432                   # Puerto por defecto de PostgreSQL
            )
            self.cursor = self.conn.cursor()
            log_info("✅ Conexión establecida exitosamente con la base de datos PostgreSQL local.")
        except Exception as e:
            log_error(f"❌ Error al conectar con PostgreSQL local: {e}")
            raise

    def cerrar_conexion(self):
        """
        Cierra el cursor y la conexión si están activos.
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            log_info("🔒 Conexión con la base de datos cerrada correctamente.")
        except Exception as e:
            log_error(f"❌ Error al cerrar la conexión: {e}")
