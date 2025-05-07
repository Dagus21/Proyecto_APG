from flask import Flask, render_template
from jinja2 import ChoiceLoader, FileSystemLoader
import os
from dotenv import load_dotenv

# Cargar variables .env
load_dotenv()

#-------------------------------------------------------------
#      CONFIGURACIÓN DEL PROYECTO APG CON ESTRUCTURA MODULAR
#-------------------------------------------------------------
app = Flask(
    __name__,
    static_folder='static',  # carpeta global para estilos compartidos
)

# Añadir múltiples carpetas de templates (públicos y base)
app.jinja_loader = ChoiceLoader([
    FileSystemLoader('Front/templates'),  # vistas públicas como inicio.html
    FileSystemLoader('templates'),        # templates base (header, footer, navbar)
    FileSystemLoader('Gestion_y_Autenticacion_Login/templates'),  # funcionalidad login
    # Puedes agregar más carpetas aquí como:
    # FileSystemLoader('funcionalidad_registro/templates'),
    # FileSystemLoader('dashboard/templates'),
])

# Clave secreta para sesiones
app.secret_key = os.getenv("FLASK_SECRET_KEY", "clave_secreta_por_defecto")

#-------------------------------------------------------------
#                  RUTAS PÚBLICAS
#-------------------------------------------------------------
@app.route('/')
def inicio():
    return render_template('inicio.html')

#-------------------------------------------------------------
#            REGISTRO DE BLUEPRINTS FUNCIONALES
#-------------------------------------------------------------
from Gestion_y_Autenticacion_Login.main import login_bp
app.register_blueprint(login_bp, url_prefix='/login')



# Puedes registrar más funcionalidades así:
# from funcionalidad_registro.main import registro_bp
# app.register_blueprint(registro_bp, url_prefix='/registro')

#-------------------------------------------------------------
#                  EJECUCIÓN LOCAL
#-------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
