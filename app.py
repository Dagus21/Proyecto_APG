import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session
from jinja2 import ChoiceLoader, FileSystemLoader
from flask_mail import Mail

#-------------------------------------------------------------
# Cargar las variables de entorno desde el archivo .env
#-------------------------------------------------------------
load_dotenv()  # Asegúrate de que las variables de entorno se carguen correctamente

# Verifica si las variables de entorno están cargadas correctamente (Eliminado para producción)
if os.getenv('EMAIL_USER') is None or os.getenv('EMAIL_PASSWORD') is None:
    raise ValueError("Correo electrónico o contraseña de aplicación no configurados correctamente en el archivo .env")

#-------------------------------------------------------------
# CONFIGURACIÓN DEL PROYECTO APG CON ESTRUCTURA MODULAR
#-------------------------------------------------------------
app = Flask(
    __name__,
    template_folder='Front/templates',  # Carpeta donde se encuentran las plantillas
    static_folder='static'              # Carpeta donde se encuentran los archivos estáticos
)

#-------------------------------------------------------------
# CONFIGURACIÓN DE LA APLICACIÓN
#-------------------------------------------------------------
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')  # Clave secreta para sesiones de Flask
app.config['MAIL_SERVER'] = os.getenv('EMAIL_SERVER')  # Servidor de correo (SMTP)
app.config['MAIL_PORT'] = int(os.getenv('EMAIL_PORT'))  # Puerto del servidor SMTP
app.config['MAIL_USE_TLS'] = True  # Usar TLS para la seguridad
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')  # Usuario de correo (normalmente el correo)
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')  # Contraseña del correo o contraseña de aplicación
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')  # Remitente del correo

# Verifica que todas las configuraciones esenciales estén presentes
required_config = ['MAIL_SERVER', 'MAIL_PORT', 'MAIL_USERNAME', 'MAIL_PASSWORD']
for key in required_config:
    if not app.config.get(key):
        raise ValueError(f"Falta la configuración de {key} en el archivo .env")

# Inicialización de Flask-Mail con la configuración proporcionada
mail = Mail(app)

#-------------------------------------------------------------
# Añadir múltiples carpetas de plantillas (públicos y base)
#-------------------------------------------------------------
app.jinja_loader = ChoiceLoader([
    app.jinja_loader,                 # Cargar la carpeta de plantillas de la aplicación
    FileSystemLoader('Front/templates'),  # Carpeta para plantillas front-end
    FileSystemLoader('templates'),        # Carpeta para plantillas base
    FileSystemLoader('Gestion_y_Autenticacion_Login/templates'),  # Carpeta de plantillas de login
    FileSystemLoader('Reestablecimiento_de_Contrasena/templates'),  # Carpeta de plantillas de reestablecimiento
])

#-------------------------------------------------------------
# REGISTRO DE BLUEPRINTS
#-------------------------------------------------------------
from Gestion_y_Autenticacion_Login.main import login_bp
from Reestablecimiento_de_Contrasena.main import reestablecer_bp

# Registro de los blueprints, que son módulos de rutas
app.register_blueprint(login_bp, url_prefix='/login')  # Ruta base para el login
app.register_blueprint(reestablecer_bp, url_prefix='/reestablecer')  # Ruta base para reestablecer contraseña

#-------------------------------------------------------------
# RUTAS PRINCIPALES
#-------------------------------------------------------------
@app.route('/')
def inicio():
    """
    Ruta principal de la aplicación.

    Devuelve la vista principal del sitio (por ejemplo, una página de inicio).
    Esta vista es accesible desde la raíz del sitio web.

    Returns:
        render_template: Renderiza la plantilla 'inicio.html'.
    """
    return render_template('inicio.html')

#-------------------------------------------------------------
# EJECUCIÓN LOCAL
#-------------------------------------------------------------
if __name__ == '__main__':
    """
    Ejecuta la aplicación Flask de manera local con soporte para SSL 
    (si se proporciona el archivo de certificados).

    Asegúrate de que el puerto esté libre y de que el host sea accesible 
    para otras máquinas si es necesario.

    El parámetro `ssl_context` se utiliza para habilitar HTTPS localmente 
    con certificados proporcionados en 'cert.pem' y 'key.pem'.
    """
    app.run(
        host='0.0.0.0',          # Escucha en todas las IPs locales
        port=2323,               # Puerto donde la aplicación escuchará
        debug=True,              # Habilita el modo de depuración para desarrollo
        ssl_context=('cert.pem', 'key.pem')  # Certificados SSL para HTTPS
    )
