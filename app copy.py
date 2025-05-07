from flask import Flask, render_template, url_for, send_from_directory, request, redirect
import os

# Configurar Flask con plantillas en el directorio raíz
app = Flask(__name__, template_folder='.')

# Configurar ruta estática para servir CSS desde templates_base/css
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('templates_base/css', filename)

# Función para crear una respuesta HTML completa usando los archivos de template
def render_with_base_templates(content_template=None, content_html=None, **context):
    # Renderizar el contenido específico si existe
    content = ""
    if content_template:
        content = render_template(content_template, **context)
    elif content_html:
        content = f'<div class="container">{content_html}</div>'
    
    # Obtener los archivos de header y footer
    with open('templates_base/header.html', 'r', encoding='utf-8') as header_file:
        header = header_file.read()
    
    with open('templates_base/footer.html', 'r', encoding='utf-8') as footer_file:
        footer = footer_file.read()
    
    # Marcar la página actual en la navegación
    current_path = context.get('current_path', '/')
    
    # Obtener el contenido del navbar
    # with open('templates_base/navbar.html', 'r', encoding='utf-8') as navbar_file:
    #     navbar = navbar_file.read()
    
    # Marcar la opción actual en el navbar
    # if current_path == '/':
    #     navbar = navbar.replace('href="/"', 'href="/" class="current"')
    # elif current_path == '/f1':
    #     navbar = navbar.replace('href="/f1"', 'href="/f1" class="current"')
    # elif current_path == '/f2':
    #     navbar = navbar.replace('href="/f2"', 'href="/f2" class="current"')
    # elif current_path == '/login':
    #     navbar = navbar.replace('href="/login"', 'href="/login" class="current"')
    
    # Reemplazar la referencia al navbar en el header
    # header = header.replace('{% include \'templates_base/navbar.html\' %}', navbar)
    
    # Combinar todas las partes
    return header + content + footer

@app.route('/')
def home():
    return render_with_base_templates(content_template='funcionalidad_login/statics/templates/funcionalidad_login_template.html', current_path='/')

@app.route('/f1')
def funcionalidad_1():
    return render_with_base_templates(content_template='funcionalidad_1/statics/templates/funcionalidad_1_template.html', current_path='/f1')

@app.route('/f2')
def funcionalidad_2():
    return render_with_base_templates(content_template='funcionalidad_2/statics/templates/funcionalidad_2_template.html', current_path='/f2')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Aquí puedes manejar la lógica de autenticación
        username = request.form['username']
        password = request.form['password']
        # Lógica de autenticación aquí
        return redirect(url_for('home'))
    return render_with_base_templates(content_template='templates_base/content.html', current_path='/login')


if __name__ == '__main__':
    app.run(debug=True)