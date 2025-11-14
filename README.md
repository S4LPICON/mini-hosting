# mini-hosting (proyecto Django)

Repositorio inicial del proyecto "mini-hosting".

Contenido:

- Backend Django en la carpeta raíz de este repo.

Notas rápidas:

- Añadir archivo `.env` con las variables de entorno necesarias (SECRET_KEY, DB, etc.).
- No subir `db.sqlite3`, `media/` ni credenciales.

Cómo ejecutar (local):

1. Crear y activar entorno virtual

   python -m venv .venv
   source .venv/bin/activate

2. Instalar dependencias

   pip install -r requirements.txt

3. Migrar y arrancar

   python manage.py migrate
   python manage.py runserver
