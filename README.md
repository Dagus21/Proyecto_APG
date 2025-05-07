
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

```bash
python app.py
```

---

## ✅ Gestión de Tests (con Pytest y Allure)

### 🧪 Estructura de Tests por funcionalidad

Cada módulo contiene su propio `test/main_test.py`. Para ejecutarlo manualmente:

```bash
python -m Gestion_y_Autenticacion_Login.test.main_test
python -m Recuperacion_y_Cambio_Contrasena.test.main_test
```

### 📊 Reportes con Allure

```bash
python -m pytest Gestion_y_Autenticacion_Login/test/main_test.py --alluredir=allure-results
allure serve allure-results
```

---

## ⚙️ Dependencias

Instala con:

```bash
pip install -r requirements.txt
```

Versión resumida del archivo `requirements.txt`: incluye Flask, bcrypt, psycopg2, flask-mail, SQLAlchemy, pytest, allure-pytest, entre otros.

---

## 👨‍💻 Autores

- Carlos Andrés Jiménez Sarmiento (CJ) – Desarrollo, estructura modular, documentación
- Moisés David Gonzales Bermúdez – Colaborador
- David Gustavo Medina Ardila – Colaborador

---

**Universidad de Pamplona - 2025**
