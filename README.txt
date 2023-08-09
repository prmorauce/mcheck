Desde la carpeta mcheck abrir un cmd y crear el entorno virtual (python -m venv D:\PMO\Personal\mcheck (Si da error revisar el archivo pyvenv.cfg cambiar los datos del usuario y la versión de Python según corresponda))
Ejecutar pip install -r requirements.txt
Una vez creado inicializar el entorno virtual, se puede acceder desde el cmd a la carpeta Scripts (no existe hasta que no crea el entorno virtual) y ejecutar el activate o el activate.bat
En el cmd regresar a la carpeta mcheck y establecer las variables para arrancar  el servidor:
set FLASK_APP=main.py
set FLASK_ENV=development
Arrancar el servidor: flask run (el puerto está definido en el main.py, línea 77)
Invocar desde el postman: http://127.0.0.1:5000/getDominantEmotion
