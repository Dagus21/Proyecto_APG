from dotenv import load_dotenv
import os

load_dotenv()

# Verificar las variables de entorno
print("MAIL_USERNAME:", os.getenv('MAIL_USERNAME'))  # Verifica el correo cargado
print("MAIL_PASSWORD:", os.getenv('MAIL_PASSWORD'))  # Verifica la contraseña cargada
