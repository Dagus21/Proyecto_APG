# Proyecto APG

Aplicación web desarrollada con **Flask**, con enfoque modular y orientado a funcionalidades reutilizables. Soporta autenticación, registro, recuperación de contraseña, verificación por correo, cambio de contraseña y más.

---

## 📁 Estructura del Proyecto

```plaintext
PROYECTO_APG/
│
├── Clases_Base/
│   ├── Conexion_Data_Base.py
│   └── Crud_Usuario_Detalle.py
│
├── Front/
│   ├── css/
│   ├── js/
│   └── templates/
│
├── Gestion_y_Autenticacion_Login/
│   ├── main.py
│   ├── GestionLogin.py
│   ├── static/
│   │   ├── css/ (login, registro, bienvenida...)
│   │   └── js/ (login.js, cambiar_contrasena.js...)
│   ├── templates/ (login.html, cambiar_contrasena.html...)
│   └── test/main_test.py
│
├── Recuperacion_y_Cambio_Contrasena/
│   ├── main.py
│   ├── helpers.py
│   ├── static/
│   ├── templates/
│   └── test/main_test.py
│
├── static/
│   ├── css/ (footer, header, navbar, styles)
│   └── js/  (enviar_verificacion.js)
│
├── templates/
│   ├── base_aux.html
│   ├── base_public.html
│   ├── base_user.html
│   ├── header.html
│   ├── footer.html
│   └── navbar.html
│
├── app.py
├── log.py
├── README.md
├── requirements.txt
└── .env
```

---

## ▶️ Ejecución de la App

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd Proyecto_APG
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
- Copiar el archivo `.env.example` a `.env`
- Configurar las variables necesarias (base de datos, correo, etc.)

5. Ejecutar la aplicación:
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

---

## ✅ Gestión de Tests (con Pytest y Allure)

### 🧪 Estructura de Tests por funcionalidad

Cada módulo contiene su propio `test/main_test.py`. Para ejecutarlo manualmente:

```bash
# Ejecutar tests de autenticación
python -m Gestion_y_Autenticacion_Login.test.main_test

# Ejecutar tests de recuperación de contraseña
python -m Recuperacion_y_Cambio_Contrasena.test.main_test

# Ejecutar todos los tests
python -m pytest
```

### 📊 Reportes con Allure

1. Generar reportes:
```bash
python -m pytest Gestion_y_Autenticacion_Login/test/main_test.py --alluredir=allure-results
```

2. Visualizar reportes:
```bash
allure serve allure-results
```

---

## ⚙️ Dependencias Principales

- Flask: Framework web
- bcrypt: Encriptación de contraseñas
- psycopg2: Conexión a PostgreSQL
- flask-mail: Envío de correos
- SQLAlchemy: ORM para base de datos
- pytest: Framework de testing
- allure-pytest: Generación de reportes

Instalar todas las dependencias:
```bash
pip install -r requirements.txt
```

---

## 🔒 Características de Seguridad

- Autenticación segura con bcrypt
- Protección contra CSRF
- Validación de correo electrónico
- Recuperación segura de contraseña
- Sesiones seguras
- Headers de seguridad configurados

---

## 👨‍💻 Autores

- Carlos Andrés Jiménez Sarmiento (CJ) – Desarrollo, estructura modular, documentación
- Moisés David Gonzales Bermúdez – Colaborador
- David Gustavo Medina Ardila – Colaborador

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

**Universidad de Pamplona - 2025**
