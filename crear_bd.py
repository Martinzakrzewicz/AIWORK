import pymysql
from getpass import getpass

HOST = "aiwork-db.cqsujejqibcg.us-east-1.rds.amazonaws.com"
USUARIO = "admin"
PUERTO = 3306
NOMBRE_BD = "aiworkdb"

password = getpass("Contraseña de RDS (no se verá al escribir): ")

try:
    conn = pymysql.connect(
        host=HOST,
        user=USUARIO,
        password=password,
        port=PUERTO,
        connect_timeout=10,
    )
    print("Conexión exitosa a RDS")

    with conn.cursor() as cur:
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS `{NOMBRE_BD}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        cur.execute("SHOW DATABASES")
        bases = [fila[0] for fila in cur.fetchall()]

    print("Bases de datos en el servidor:", bases)
    if NOMBRE_BD in bases:
        print(f"La base '{NOMBRE_BD}' existe y está lista")
    conn.close()

except pymysql.err.OperationalError as e:
    codigo = e.args[0]
    if codigo == 1045:
        print("Error: usuario o contraseña incorrectos.")
    elif codigo in (2003, 2013):
        print("Error de red: revisa el Security Group y que la instancia esté 'Disponible'.")
    else:
        print("Error de MySQL:", e)