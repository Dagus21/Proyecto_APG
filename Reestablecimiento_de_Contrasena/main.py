# Reestablecimiento_de_Contrasena/main.py

#-------------------------------------------------------------
# IMPORTACIONES NECESARIAS
#-------------------------------------------------------------
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from Reestablecimiento_de_Contrasena.ReestablecerContrasena import ReestablecerContrasena
import os
from jinja2 import Template
import logging
from dotenv import load_dotenv
from flask_mail import Message

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#-------------------------------------------------------------
# BLUEPRINT Y GESTOR
#-------------------------------------------------------------
reestablecer_bp = Blueprint(
    'reestablecer',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/reestablecer/static'
)

reestablecer_manager = ReestablecerContrasena()

#-------------------------------------------------------------
# RUTAS
#-------------------------------------------------------------
@reestablecer_bp.route('/')
def vista_reestablecer():
    """Muestra el formulario de reestablecimiento de contraseña"""
    mensaje = request.args.get('mensaje', '')
    return render_template('Reestablecer_Contrasena.html', mensaje=mensaje)

@reestablecer_bp.route('/solicitar', methods=['POST'])
def solicitar_reestablecimiento():
    try:
        email = request.form.get('email')
        
        if not email:
            return jsonify({
                "status": 400,
                "mensaje": "❌ Se requiere el correo electrónico."
            }), 400

        # SOLO LLAMA EL MÉTODO, él ya envía el correo
        controlador = ReestablecerContrasena()
        resultado = controlador.solicitar_reestablecimiento(email)

        return jsonify(resultado), resultado["status"]

    except Exception as e:
        logger.error(f"Error en solicitar_reestablecimiento: {str(e)}")
        return jsonify({
            "status": 500,
            "mensaje": "❌ Error al procesar la solicitud."
        }), 500


@reestablecer_bp.route('/cambiar/<token>', methods=['GET', 'POST'])
def cambiar_contrasena(token):
    try:
        controlador = ReestablecerContrasena()

        if request.method == 'GET':
            # Verificar el token
            resultado = controlador.verificar_token(token)
            if resultado["status"] != 200:
                logger.error(f"Token no válido: {resultado['mensaje']}")
                return redirect(url_for('reestablecer.vista_reestablecer', mensaje=resultado["mensaje"]))

            return render_template('actualizar_contrasena.html', token=token)

        # POST: Procesar el cambio de contraseña
        nueva_contrasena = request.form.get('nueva_contrasena')
        confirmar_contrasena = request.form.get('confirmar_contrasena')

        if not nueva_contrasena or not confirmar_contrasena:
            logger.error("Faltan los campos de contraseña.")
            return render_template(
                'actualizar_contrasena.html',
                token=token,
                mensaje="❌ Todos los campos son requeridos."
            )

        if nueva_contrasena != confirmar_contrasena:
            logger.error("Las contraseñas no coinciden.")
            return render_template(
                'actualizar_contrasena.html',
                token=token,
                mensaje="❌ Las contraseñas no coinciden."
            )

        resultado = controlador.reestablecer_contrasena(token, nueva_contrasena)

        if resultado["status"] == 200:
            # ¡Contraseña cambiada!
            return render_template('Contrasena_Cambiada_Exito.html')
        else:
            # Mostrar el error en el mismo formulario
            return render_template(
                'actualizar_contrasena.html',
                token=token,
                mensaje=resultado["mensaje"]
            )

    except Exception as e:
        logger.error(f"Error en actualizar_contrasena: {str(e)}")
        return redirect(url_for('reestablecer.vista_reestablecer', mensaje="❌ Error al procesar la solicitud."))
