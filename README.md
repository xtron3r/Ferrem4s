
🛠️ Ferremas - Proyecto de Programación Web

¡Bienvenido al repositorio del proyecto Ferremas! Este proyecto fue desarrollado como parte del curso de Integración de Plataformas y tiene como objetivo ofrecer una plataforma funcional con integraciones de apis externas como Transbank y Banco Central. Usando Django con una base de datos Oracle.

📦 Acerca del Proyecto
Este repositorio contiene todo el código fuente y los scripts necesarios para ejecutar Ferremas, una aplicación web para gestión de productos, usuarios y funcionalidades administrativas.

🚀 Requisitos Previos
- Python 3.11
- Oracle SQL Developer
- C++ Build Tools (necesarios para algunas librerías como cx_Oracle)
- Acceso a una base de datos Oracle

⚙️ Instrucciones de Instalación



1. Crear un entorno virtual:
   py -3.11 -m venv venv
   venv\Scripts\activate  # En Windows
   source venv/bin/activate  # En Linux/macOS

2. Instalar las dependencias:
   pip install -r requirements.txt

3. Configurar la base de datos:
   - Usar Oracle SQL Developer para ejecutar el script que crea el usuario y da permisos. 
   - ( COMANDOS CREACION DE USUARIO Y PERMISOS )
        alter session set "_ORACLE_SCRIPT"=true

        create user Ferremas identified by ferre123;

        GRANT CONNECT, RESOURCE TO Ferremas;

        ALTER USER Ferremas QUOTA UNLIMITED ON USERS;
        ALTER USER Ferremas DEFAULT TABLESPACE USERS;
        ALTER USER Ferremas TEMPORARY TABLESPACE TEMP;

   - Asegúrate de que tu archivo settings.py esté correctamente configurado con los datos de conexión a Oracle.

4. Aplicar migraciones:
   python manage.py makemigrations
   python manage.py migrate

5. Cargar datos iniciales:
   - Ejecuta el script SQL que carga los productos, usuarios u otros registros iniciales.

6. Crear superusuario (opcional):
   python manage.py createsuperuser

7. Ejecutar el servidor:
   python manage.py runserver



📫 Contacto
- Aarón Leal
  - Email: aaronleal03@gmail.com
  - LinkedIn: [Aarón]()

- Gibrán Beiza
  - Email: gib.beiza@duocuc.cl
  - LinkedIn: [Gibrán]()

Proyecto realizado para el curso de Integración de Plataformas - Duoc UC
