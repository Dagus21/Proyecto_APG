import bcrypt
from flask import Blueprint, render_template, request, jsonify, redirect, session, url_for
from Gestion_y_Autenticacion_Login.GestionLogin import GestionLogin

#-------------------------------------------------------------
#                Blueprint y Gestor de Login
#-------------------------------------------------------------
login_bp = Blueprint(
    'login',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/login_static'
)

login_manager = GestionLogin()

#-------------------------------------------------------------
#                      RUTAS DE LOGIN
#-------------------------------------------------------------

@login_bp.route('/', methods=['GET'])
def vista_login():
    mensaje = request.args.get("mensaje", "")
    return render_template('login.html', mensaje=mensaje)

@login_bp.route('/iniciar', methods=['POST'])
def login_usuario():
    datos = request.form
    resultado = login_manager.login_usuario(datos)

    if resultado["status"] == 200:
        return redirect('/login/bienvenida')

    session['mensaje_error'] = resultado['mensaje']
    return redirect('/login/')


@login_bp.route('/cerrar', methods=['GET'])
def cerrar_sesion():
    """Cierra la sesión del usuario"""
    resultado = login_manager.cerrar_sesion()

    if resultado["status"] == 200:
        return redirect(url_for('login.vista_login'))
    else:
        return jsonify(resultado), 500  # Para mostrar errores si algo falla



@login_bp.route('/bienvenida', methods=['GET'])
def bienvenida_usuario():
    """Vista protegida que requiere autenticación"""
    if not session.get("autenticado"):
        return redirect('/login')

    usuario = {
        "id_usuario": session.get("id_usuario"),
        "nick_name": session.get("nick_name"),
        "estado_cuenta": session.get("estado_cuenta")
    }

    return render_template("bienvenida.html", usuario=usuario)


#-------------------------------------------------------------
#                   RUTAS DE REGISTRO
#-------------------------------------------------------------

@login_bp.route('/registro', methods=['GET'])
def vista_registro():
    """Muestra el formulario de registro"""
    return render_template("registro.html")


@login_bp.route('/registrar', methods=['POST'])
def registrar_usuario():
    """Registra un nuevo usuario desde JSON"""
    datos = request.json
    resultado = login_manager.crear_usuario_con_detalle(datos)
    return jsonify(resultado)


#-------------------------------------------------------------
#            VERIFICACIÓN DE CUENTA POR CORREO
#-------------------------------------------------------------

@login_bp.route('/verificar/<token>')
def verificar(token):
    resultado = login_manager.verificar_token(token)
    if resultado["status"] == 200:
        return render_template("verificacion_email.html")
    return jsonify(resultado)


@login_bp.route('/enviar-verificacion', methods=['POST'])
def enviar_correo_verificacion():
    if not session.get("autenticado"):
        return jsonify({"status": 401, "mensaje": "No autenticado."})

    correo = session.get("email")
    nick_name = session.get("nick_name")
    resultado = login_manager.enviar_correo_verificacion(correo, nick_name)
    return jsonify(resultado)


#-------------------------------------------------------------
#                  CAMBIO DE CONTRASEÑA
#-------------------------------------------------------------

@login_bp.route('/cambiar-contrasena', methods=['GET', 'POST'])
def cambiar_contrasena():
    if not session.get("autenticado"):
        return redirect('/login')

    mensaje = request.args.get("mensaje") or ""
    id_usuario = session.get("id_usuario")

    if request.method == "POST":
        actual = request.form["actual"]
        nueva = request.form["nueva"]
        confirmar = request.form["confirmar"]

        if nueva != confirmar:
            mensaje = "⚠️ Las nuevas contraseñas no coinciden."
        else:
            datos = login_manager.leer_por_usuario(id_usuario)
            if datos["status"] != 200 or datos["data"] is None:
                mensaje = "❌ Usuario no encontrado."
            else:
                hash_guardado = datos["data"]["contrasena"]
                if not bcrypt.checkpw(actual.encode("utf-8"), hash_guardado.encode("utf-8")):
                    mensaje = "❌ La contraseña actual no es correcta."
                else:
                    resultado = login_manager.actualizar_usuario_con_detalle(id_usuario, {"contrasena": nueva})
                    if resultado["status"] == 200:
                        return redirect(url_for('login.cambiar_contrasena', mensaje="✅ Contraseña actualizada correctamente."))
                    mensaje = f"❌ {resultado['mensaje']}"

    usuario = {
        "id_usuario": session.get("id_usuario"),
        "nick_name": session.get("nick_name"),
        "estado_cuenta": session.get("estado_cuenta")
    }
    return render_template("cambiar_contrasena.html", mensaje=mensaje, usuario=usuario)
