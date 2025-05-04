#-------------------------------------------------------------
#         Test de conexión y exploración de base de datos
#-------------------------------------------------------------
"""
Autor: Carlos Andrés Jiménez Sarmiento (CJ)

Descripción:
Este test automatizado valida la conexión a la base de datos PostgreSQL
y explora su estructura: tablas, columnas, claves primarias y foráneas.

Además, ejecuta pruebas unitarias para las operaciones CRUD del módulo
Crud_Usuario_Detalle.

Compatible con Pytest y Allure. Ejecutable también de forma manual.
"""

import pytest
import allure
from Clases_Base.Conexion_Data_Base import Conexion_Data_Base
from Clases_Base.Crud_Usuario_Detalle import CrudUsuarioDetalle
from log import log_info, log_error, log_success

#-------------------------------------------------------------
#                    TEST EXPLORACIÓN DE ESTRUCTURA
#-------------------------------------------------------------

def test_explorar_estructura_bd():
    """
    Ejecuta una consulta que explora todas las tablas, columnas,
    claves primarias y foráneas de la base de datos.
    """
    conexion = Conexion_Data_Base()
    try:
        conexion.conectar()

        conexion.cursor.execute("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
            ORDER BY table_schema, table_name;
        """)
        tablas = conexion.cursor.fetchall()
        log_success(f"Se encontraron {len(tablas)} tablas.")
        assert len(tablas) > 0

        for schema, tabla in tablas:
            log_info(f"\n📄 Tabla: {schema}.{tabla}")

            conexion.cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = %s AND table_schema = %s
                ORDER BY ordinal_position;
            """, (tabla, schema))
            columnas = conexion.cursor.fetchall()
            for col in columnas:
                log_info(f"    - {col[0]} ({col[1]}, NULLABLE: {col[2]})")

            conexion.cursor.execute("""
                SELECT kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                  ON tc.constraint_name = kcu.constraint_name
                WHERE tc.constraint_type = 'PRIMARY KEY'
                  AND tc.table_name = %s AND tc.table_schema = %s;
            """, (tabla, schema))
            for pk in conexion.cursor.fetchall():
                log_info(f"    🔑 PRIMARY KEY: {pk[0]}")

            conexion.cursor.execute("""
                SELECT kcu.column_name, ccu.table_schema, ccu.table_name, ccu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                  ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage ccu
                  ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY'
                  AND tc.table_name = %s AND tc.table_schema = %s;
            """, (tabla, schema))
            for fk in conexion.cursor.fetchall():
                log_info(f"    🔗 FOREIGN KEY: {fk[0]} → {fk[1]}.{fk[2]}.{fk[3]}")

        log_success("Exploración de estructura completada correctamente.")
        assert True

    except Exception as e:
        log_error(f"❌ Error durante la exploración: {e}")
        assert False
    finally:
        conexion.cerrar_conexion()
        log_info("Exploración finalizada.")

#-------------------------------------------------------------
#                        TESTS DE CRUD
#-------------------------------------------------------------

def test_crud_crear():
    data = {
        "nick_name": "Carlos_CJ",
        "contrasena": "1234",
        "email": "carjisar@gmail.com"
    }
    crud = CrudUsuarioDetalle()
    try:
        print(crud.crear_usuario_con_detalle(data))
        log_info("Usuario creado correctamente.")
        log_success("CRUD test ejecutado correctamente.")
    except Exception as e:
        log_error(f"❌ Error en el CRUD test: {e}")
    finally:
        log_info("CRUD test finalizado.")

def test_crud_leer_todos():
    crud = CrudUsuarioDetalle()
    try:
        print(crud.leer_usuarios_con_detalle())
        log_success("CRUD test ejecutado correctamente.")
    except Exception as e:
        log_error(f"❌ Error en el CRUD test: {e}")
    finally:
        log_info("CRUD test finalizado.")

def test_crud_leer_por_id():
    crud = CrudUsuarioDetalle()
    try:
        print(crud.leer_por_usuario(4))
        log_success("CRUD test ejecutado correctamente.")
    except Exception as e:
        log_error(f"❌ Error en el CRUD test: {e}")
    finally:
        log_info("CRUD test finalizado.")

def test_crud_actualizar():
    data = { "contrasena": "12345678" }
    crud = CrudUsuarioDetalle()
    try:
        print(crud.actualizar_usuario_con_detalle(4, data))
        log_success("CRUD test ejecutado correctamente.")
    except Exception as e:
        log_error(f"❌ Error en el CRUD test: {e}")
    finally:
        log_info("CRUD test finalizado.")

#-------------------------------------------------------------
#                TEST AUTOMÁTICO PARA PYTEST + ALLURE
#-------------------------------------------------------------

@allure.feature("Base de Datos")
@allure.title("Verifica conexión y estructura general de la base de datos")
def test_answer():
    assert test_explorar_estructura_bd() is None  # Usa asserts internos

#-------------------------------------------------------------
#            EJECUCIÓN MANUAL (para pruebas locales)
#-------------------------------------------------------------

if __name__ == "__main__":
    try:
        test_answer()
    except Exception as e:
        log_error(f"❌ Error al ejecutar manualmente: {e}")
