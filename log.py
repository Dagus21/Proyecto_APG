#-------------------------------------------------------------
#                    Librerías e Importaciones
#-------------------------------------------------------------
"""
Módulo de logging estructurado para el proyecto Proyecto_APG.

- logging: Para definir y gestionar múltiples niveles de log.
- os: Para rutas de archivo dinámicas.
- inspect: Para identificar automáticamente el archivo llamador.
- datetime: Para formato de fechas en logs especiales como documentación.

Autor: Carlos Andrés Jiménez Sarmiento (CJ)
"""

import logging
import os
import inspect
from datetime import datetime

#-------------------------------------------------------------
#                   VARIABLES GLOBALES DE LOG
#-------------------------------------------------------------
"""
Configuración base para el sistema de logging estructurado.

- PROYECTO_RAIZ: Nombre raíz del directorio donde se agrupan todas las funcionalidades.
- LOG_FORMAT: Formato de los mensajes de log (incluye nivel, archivo y línea).
- FECHA_HORA_FORMATO_DOC: Formato especial para los logs de documentación.
- NOMBRE_ARCHIVO_LOG: Nombre base que tendrá el archivo de log global del proyecto.
"""

PROYECTO_RAIZ = 'Proyecto_APG'
LOG_FORMAT = '%(asctime)s - %(levelname)s - Archivo: %(filename)s - Línea: %(lineno)d - %(message)s'
FECHA_HORA_FORMATO_DOC = '%d/%m/%Y %I:%M %p'
NOMBRE_ARCHIVO_LOG = 'APG.log'

#-------------------------------------------------------------
#                    FUNCIONES INTERNAS
#-------------------------------------------------------------

def _archivo_llamador():
    """
    Devuelve el nombre del archivo (.py) que invocó la función log.
    Se utiliza para añadir trazabilidad en los mensajes.
    """
    frame = inspect.stack()[3]
    return os.path.basename(frame.filename)

def _configurar_logger(nivel_nombre='GENERAL'):
    """
    Configura un logger único global para todo el proyecto.
    El archivo de log siempre se guarda en la raíz del proyecto.

    Args:
        nivel_nombre (str): Etiqueta de nivel para el logger.

    Returns:
        logging.Logger: Logger configurado y reutilizable.
    """
    # Obtener la ruta absoluta a la raíz del proyecto
    ruta_script_actual = os.path.abspath(__file__)
    partes = ruta_script_actual.split(os.sep)

    if PROYECTO_RAIZ in partes:
        idx = partes.index(PROYECTO_RAIZ)
        ruta_raiz = os.sep.join(partes[:idx + 1])
    else:
        ruta_raiz = os.getcwd()  # Fallback por seguridad

    ruta_log = os.path.join(ruta_raiz, NOMBRE_ARCHIVO_LOG)

    logger = logging.getLogger(f"{PROYECTO_RAIZ}_{nivel_nombre}")
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():
        formatter = logging.Formatter(LOG_FORMAT)

        file_handler = logging.FileHandler(ruta_log, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

#-------------------------------------------------------------
#               FUNCIONES DE LOG DE USO PÚBLICO
#-------------------------------------------------------------

def log_debug(mensaje: str):
    logger = _configurar_logger('DEBUG')
    archivo = _archivo_llamador()
    mensaje_log = f"[DEBUG] [{archivo}] {mensaje}"
    logger.debug(mensaje_log)
    print(mensaje_log)

def log_info(mensaje: str):
    logger = _configurar_logger('INFO')
    archivo = _archivo_llamador()
    mensaje_log = f"[INFO] [{archivo}] {mensaje}"
    logger.info(mensaje_log)
    print(mensaje_log)

def log_warning(mensaje: str):
    logger = _configurar_logger('WARNING')
    archivo = _archivo_llamador()
    mensaje_log = f"[WARNING] [{archivo}] {mensaje}"
    logger.warning(mensaje_log)
    print(mensaje_log)

def log_error(mensaje: str):
    logger = _configurar_logger('ERROR')
    archivo = _archivo_llamador()
    mensaje_log = f"[ERROR] [{archivo}] {mensaje}"
    logger.error(mensaje_log)
    print(mensaje_log)

def log_critical(mensaje: str):
    logger = _configurar_logger('CRITICAL')
    archivo = _archivo_llamador()
    mensaje_log = f"[CRITICAL] [{archivo}] {mensaje}"
    logger.critical(mensaje_log)
    print(mensaje_log)

def log_documentacion(mensaje: str):
    logger = _configurar_logger('DOCUMENTACION')
    archivo = _archivo_llamador()
    fecha_hora = datetime.now().strftime(FECHA_HORA_FORMATO_DOC)
    mensaje_log = f"[DOC] {fecha_hora} - [{archivo}] {mensaje}"
    logger.info(mensaje_log)
    print(mensaje_log)

def log_success(mensaje: str):
    logger = _configurar_logger('SUCCESS')
    archivo = _archivo_llamador()
    mensaje_log = f"[SUCCESS] [{archivo}] {mensaje}"
    logger.info(mensaje_log)
    print(mensaje_log)


