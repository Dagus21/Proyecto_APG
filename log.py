#-------------------------------------------------------------
#                   LIBRERÍAS E IMPORTACIONES
#-------------------------------------------------------------
"""
Módulo: Log_Ciproba.py

Sistema de logging estructurado, reutilizable y configurable para proyectos Python.

Incluye múltiples niveles de log:
- DEBUG, INFO, WARNING, ERROR, CRITICAL
- SUCCESS (éxito) y DOCUMENTACION (registro técnico)

Características:
- Guarda los logs en una ruta personalizada o, por defecto, junto al archivo.
- Registro automático del archivo que ejecuta la acción y su línea.
- Registro en consola y archivo con el mismo formato.
- Personalización mediante variables globales al inicio del módulo.
- Integración profesional con scripts, automatizaciones y orquestaciones externas.

Variables configurables:
- `RUTA_LOG_PERSONALIZADA`: ruta donde se guardarán los logs (si es None, se usará la ruta local).
- `NOMBRE_ARCHIVO_LOG`: nombre del archivo .log generado.
- `LOG_FORMAT`: formato del mensaje en los logs.
- `FORMATO_FECHA_DOC`: formato humanizado de fecha para registros técnicos.

Autor: Carlos Andrés Jiménez Sarmiento (CJ)
"""

import logging
import os
import inspect
from datetime import datetime

#-------------------------------------------------------------
#              VARIABLES CONFIGURABLES DEL USUARIO
#-------------------------------------------------------------

RUTA_LOG_PERSONALIZADA = None  # Ejemplo: r"C:\Logs\MiProyecto"
NOMBRE_ARCHIVO_LOG = 'APG.log'

LOG_FORMAT = '%(asctime)s - %(levelname)s - Archivo: %(filename)s - Línea: %(lineno)d - %(message)s'
FORMATO_FECHA_DOC = '%d/%m/%Y %I:%M %p'

#-------------------------------------------------------------
#                    FUNCIONES INTERNAS
#-------------------------------------------------------------

def _archivo_llamador():
    """
    Obtiene el nombre del archivo (.py) que llamó directamente a la función de log.

    Returns:
        str: nombre del archivo desde donde se originó la llamada al log.
    """
    stack = inspect.stack()
    if len(stack) > 3:
        return os.path.basename(stack[3].filename)
    elif len(stack) > 1:
        return os.path.basename(stack[1].filename)
    return "desconocido"

def _configurar_logger(nivel_nombre='GENERAL'):
    """
    Crea y configura un logger reutilizable por nivel.

    - Si `RUTA_LOG_PERSONALIZADA` está definida, los logs se guardan allí.
    - Si no, se guardan en la misma ruta del archivo actual (`Log_Ciproba.py`).
    - El logger usa consola y archivo con el mismo formato definido en `LOG_FORMAT`.

    Args:
        nivel_nombre (str): Identificador interno del tipo de log (DEBUG, INFO...).

    Returns:
        logging.Logger: instancia configurada lista para uso inmediato.
    """
    ruta_base = RUTA_LOG_PERSONALIZADA or os.path.dirname(os.path.abspath(__file__))
    ruta_log = os.path.join(ruta_base, NOMBRE_ARCHIVO_LOG)

    os.makedirs(os.path.dirname(ruta_log), exist_ok=True)

    logger = logging.getLogger(f"APG_{nivel_nombre}")
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():
        formatter = logging.Formatter(LOG_FORMAT)

        # Handler archivo
        file_handler = logging.FileHandler(ruta_log, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Handler consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

#-------------------------------------------------------------
#                  FUNCIONES DE LOG PÚBLICAS
#-------------------------------------------------------------

def log_debug(mensaje: str):
    """
    Registra un mensaje de depuración (nivel DEBUG).

    Args:
        mensaje (str): texto a registrar.
    """
    logger = _configurar_logger('DEBUG')
    archivo = _archivo_llamador()
    mensaje_log = f"[DEBUG] [{archivo}] {mensaje}"
    logger.debug(mensaje_log)
    print(mensaje_log)

def log_info(mensaje: str):
    """
    Registra un mensaje informativo (nivel INFO).

    Args:
        mensaje (str): texto a registrar.
    """
    logger = _configurar_logger('INFO')
    archivo = _archivo_llamador()
    mensaje_log = f"[INFO] [{archivo}] {mensaje}"
    logger.info(mensaje_log)
    print(mensaje_log)

def log_warning(mensaje: str):
    """
    Registra una advertencia no crítica (nivel WARNING).

    Args:
        mensaje (str): texto a registrar.
    """
    logger = _configurar_logger('WARNING')
    archivo = _archivo_llamador()
    mensaje_log = f"[WARNING] [{archivo}] {mensaje}"
    logger.warning(mensaje_log)
    print(mensaje_log)

def log_error(mensaje: str):
    """
    Registra un error grave (nivel ERROR).

    Args:
        mensaje (str): texto a registrar.
    """
    logger = _configurar_logger('ERROR')
    archivo = _archivo_llamador()
    mensaje_log = f"[ERROR] [{archivo}] {mensaje}"
    logger.error(mensaje_log)
    print(mensaje_log)

def log_critical(mensaje: str):
    """
    Registra un error crítico (nivel CRITICAL), potencialmente bloqueante.

    Args:
        mensaje (str): texto a registrar.
    """
    logger = _configurar_logger('CRITICAL')
    archivo = _archivo_llamador()
    mensaje_log = f"[CRITICAL] [{archivo}] {mensaje}"
    logger.critical(mensaje_log)
    print(mensaje_log)

def log_documentacion(mensaje: str):
    """
    Registra información técnica o explicativa relevante (nivel INFO),
    con marca de tiempo en formato humanizado.

    Args:
        mensaje (str): texto a registrar.
    """
    logger = _configurar_logger('DOCUMENTACION')
    archivo = _archivo_llamador()
    fecha_hora = datetime.now().strftime(FORMATO_FECHA_DOC)
    mensaje_log = f"[DOC] {fecha_hora} - [{archivo}] {mensaje}"
    logger.info(mensaje_log)
    print(mensaje_log)

def log_success(mensaje: str):
    """
    Registra un mensaje de éxito o confirmación personalizada (nivel INFO).

    Args:
        mensaje (str): texto a registrar.
    """
    logger = _configurar_logger('SUCCESS')
    archivo = _archivo_llamador()
    mensaje_log = f"[SUCCESS] [{archivo}] {mensaje}"
    logger.info(mensaje_log)
    print(mensaje_log)
