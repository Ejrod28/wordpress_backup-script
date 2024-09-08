import os
import subprocess
import datetime
import tarfile

# Configuración
WP_DIR = '/var/www/html/wordpress'  # Ruta al directorio de WordPress
BACKUP_DIR = '/var/backups/wordpress'     # Ruta donde se guardarán los respaldos
DB_NAME = 'wordpress_db'    # Nombre de la base de datos
DB_USER = 'wordpress_user'   # Usuario de la base de datos
DB_PASS = 'wordpressSuperSecurePassword' # Contraseña de la base de datos
DATE = datetime.datetime.now().strftime('%F_%H-%M-%S')
BACKUP_FILENAME = f'wordpress_backup_{DATE}.tar.gz'

# Crear directorio de respaldo si no existe
os.makedirs(BACKUP_DIR, exist_ok=True)

# Copia de seguridad de archivos de WordPress
print('Realizando copia de seguridad de los archivos de WordPress...')
files_backup_path = os.path.join(BACKUP_DIR, f'wordpress_files_{DATE}.tar.gz')
with tarfile.open(files_backup_path, 'w:gz') as tar:
    tar.add(WP_DIR, arcname=os.path.basename(WP_DIR))

# Respaldo de la base de datos
print('Realizando respaldo de la base de datos...')
db_backup_path = os.path.join(BACKUP_DIR, f'wordpress_db_{DATE}.sql')
try:
    subprocess.run(
        ['mysqldump', '-u', DB_USER, '-p' + DB_PASS, DB_NAME],
        check=True,
        stdout=open(db_backup_path, 'w')
    )
except subprocess.CalledProcessError as e:
    print(f'Error al realizar el respaldo de la base de datos: {e}')
    exit(1)

# Generar archivo comprimido con todos los respaldos
print('Generando archivo comprimido con todos los respaldos...')
with tarfile.open(os.path.join(BACKUP_DIR, BACKUP_FILENAME), 'w:gz') as tar:
    tar.add(files_backup_path, arcname=os.path.basename(files_backup_path))
    tar.add(db_backup_path, arcname=os.path.basename(db_backup_path))

# Limpiar archivos temporales
print('Limpiando archivos temporales...')
os.remove(files_backup_path)
os.remove(db_backup_path)

print(f'Copia de seguridad completada. El archivo comprimido está en {os.path.join(BACKUP_DIR, BACKUP_FILENAME)}')