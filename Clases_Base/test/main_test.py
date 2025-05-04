#-------------------------------------------------------------
#     Test: Conexión y Exploración de Base de Datos + CRUD
#-------------------------------------------------------------
"""
Autor: Carlos Andrés Jiménez Sarmiento (CJ)

Descripción:
Este archivo realiza pruebas automáticas para:

1. Validar conexión a la base de datos PostgreSQL.
2. Explorar estructura de tablas, columnas, claves primarias y foráneas.
3. Ejecutar operaciones CRUD básicas sobre las tablas `usuarios` y `detalle_usuarios`.

Compatible con Pytest y Allure. También se puede ejecutar manualmente.
Ubicación: Clases_Base/test/test_exploracion_crud.py
"""

import pytest
import allure
from Clases_Base.Conexion_Data_Base import Conexion_Data_Base
from Clases_Base.Crud_Usuario_Detalle import CrudUsuarioDetalle
from log import log_info, log_error, log_success

#-------------------------------------------------------------
#               TEST 1: EXPLORACIÓN DE ESTRUCTURA BD
#-------------------------------------------------------------

@allure.feature("Base de Datos")
@allure.title("Explora tablas, columnas y claves en la base de datos")
def test_explorar_estructura_bd():
    """
    Explora tablas, columnas, claves primarias y foráneas de la base de datos.
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
        log_success(f"🧩 Se encontraron {len(tablas)} tablas.")
        assert len(tablas) > 0

        for schema, tabla in tablas:
            log_info(f"\n📄 Tabla: {schema}.{tabla}")

            # Columnas
            conexion.cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = %s AND table_schema = %s
                ORDER BY ordinal_position;
            """, (tabla, schema))
            columnas = conexion.cursor.fetchall()
            for col in columnas:
                log_info(f"    - {col[0]} ({col[1]}, NULLABLE: {col[2]})")

            # Claves primarias
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

            # Claves foráneas
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

        log_success("✅ Exploración de estructura completada.")
    except Exception as e:
        log_error(f"❌ Error durante la exploración: {e}")
        assert False
    finally:
        conexion.cerrar_conexion()
        log_info("🧪 Test de exploración finalizado.")

#-------------------------------------------------------------
#                   TESTS CRUD DE USUARIO
#-------------------------------------------------------------

@allure.feature("CRUD")
@allure.title("Crear nuevo usuario con detalle")
def test_crud_crear():
    crud = CrudUsuarioDetalle()
    data = {
        "nick_name": "Carlos_CJ",
        "contrasena": "1234",
        "email": "carjisar@gmail.com"
    }
    try:
        resultado = crud.crear_usuario_con_detalle(data)
        print("Resultado crear:", resultado)
        assert resultado["status"] == 201
        log_success("✅ Usuario creado correctamente.")
    except Exception as e:
        log_error(f"❌ Error al crear usuario: {e}")
        assert False

@allure.feature("CRUD")
@allure.title("Leer todos los usuarios con detalle")
def test_crud_leer_todos():
    crud = CrudUsuarioDetalle()
    try:
        resultado = crud.leer_usuarios_con_detalle()
        print("Resultado leer todos:", resultado)
        assert resultado["status"] == 200
        log_success("✅ Usuarios leídos correctamente.")
    except Exception as e:
        log_error(f"❌ Error al leer usuarios: {e}")
        assert False

@allure.feature("CRUD")
@allure.title("Leer usuario por ID (o email/nick)")
def test_crud_leer_por_id():
    crud = CrudUsuarioDetalle()
    try:
        resultado = crud.leer_por_usuario(4)  # Puede ser int, email o nick
        print("Resultado leer usuario:", resultado)
        assert resultado["status"] == 200
        log_success("✅ Usuario consultado correctamente.")
    except Exception as e:
        log_error(f"❌ Error al consultar usuario: {e}")
        assert False

@allure.feature("CRUD")
@allure.title("Actualizar datos del usuario")
def test_crud_actualizar():
    crud = CrudUsuarioDetalle()
    data = {
            "estado_cuenta": True,
            }
    try:
        resultado = crud.actualizar_usuario_con_detalle("carjisar@gmail.com", data)
        print("Resultado actualizar:", resultado)
        assert resultado["status"] == 200
        log_success("✅ Usuario actualizado correctamente.")
    except Exception as e:
        log_error(f"❌ Error al actualizar usuario: {e}")
        assert False
        
@allure.feature("CRUD")
@allure.title("Eliminar usuario por Criterio")
def test_crud_eliminar():
    crud = CrudUsuarioDetalle()
    try:
        resultado = crud.eliminar_usuario_con_detalle(5)  # Puede ser int, email o nick
        print("Resultado eliminar:", resultado)
        assert resultado["status"] == 200
        log_success("✅ Usuario eliminado correctamente.")
    except Exception as e:
        log_error(f"❌ Error al eliminar usuario: {e}")
        assert False

#-------------------------------------------------------------
#               EJECUCIÓN MANUAL DE PRUEBAS
#-------------------------------------------------------------

if __name__ == "__main__":
    try:
        #print("\n🔎 Exploración de BD")
        #test_explorar_estructura_bd()

        #print("\n🛠️ Crear usuario")
        #test_crud_crear()

        #print("\n✏️ Actualizar usuario")
        #test_crud_actualizar()
        
        #print("\n🔍 Leer usuario por ID")
        #test_crud_leer_por_id()
        
        #print("\n🗑️ Eliminar usuario")
        #test_crud_eliminar()
        
        print("\n📋 Leer todos los usuarios")
        test_crud_leer_todos()
        
    except Exception as e:
        log_error(f"❌ Error general al ejecutar manualmente: {e}")
