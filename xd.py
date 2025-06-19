import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Verificar si la variable se está cargando correctamente
print(os.getenv("DIRECCION_URL"))
