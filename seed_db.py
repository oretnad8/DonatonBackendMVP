import mysql.connector
import bcrypt
import uuid

def hash_password(password):
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

import time

def seed_db():
    print("Conectando a base de datos...")
    
    # Retry loop para esperar a que los microservicios creen las tablas
    max_retries = 20
    
    # Primero asegurarse de que la base de datos exista con UTF8
    try:
        temp_conn = mysql.connector.connect(host="localhost", user="root", password="")
        temp_cursor = temp_conn.cursor()
        temp_cursor.execute("CREATE DATABASE IF NOT EXISTS donaton_db CHARACTER SET utf8 COLLATE utf8_general_ci")
        temp_conn.commit()
        temp_conn.close()
    except Exception as e:
        print(f"Error asegurando creación de BD: {e}")

    conn = None
    for i in range(max_retries):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="donaton_db",
                charset="utf8"
            )
            cursor = conn.cursor()
            # Verificar si TODAS las tablas ya fueron creadas por Hibernate
            cursor.execute("SHOW TABLES LIKE 'usuarios'")
            has_usuarios = cursor.fetchone()
            cursor.execute("SHOW TABLES LIKE 'necesidades'")
            has_necesidades = cursor.fetchone()
            cursor.execute("SHOW TABLES LIKE 'stock'")
            has_stock = cursor.fetchone()
            
            if has_usuarios and has_necesidades and has_stock:
                print("Tablas detectadas. Procediendo con el seeding...")
                break
            else:
                print(f"[{i+1}/{max_retries}] Base de datos conectada, pero faltan tablas (usuarios:{bool(has_usuarios)}, nec:{bool(has_necesidades)}, stock:{bool(has_stock)}). Esperando 5 segundos...")
                conn.close()
                time.sleep(5)
        except mysql.connector.Error as err:
            print(f"[{i+1}/{max_retries}] Error conectando a la BD: {err}. Esperando 5 segundos...")
            time.sleep(5)
    else:
        print("Error crítico: Las tablas no fueron creadas después de 100 segundos. Abortando seed.")
        return

    print("Seeding usuarios...")
    
    # Usuarios (UUID -> binary(16))
    users = [
        (str(uuid.uuid4()), "11111111-1", "Admin", "Donaton", "admin@donaton.cl", hash_password("admin123"), "ADMIN_SENAPRED", True),
        (str(uuid.uuid4()), "22222222-2", "Coordinador", "Bodega", "coordinador@donaton.cl", hash_password("coord123"), "JEFE_BODEGA", True),
        (str(uuid.uuid4()), "33333333-3", "Voluntario", "Terreno", "voluntario@donaton.cl", hash_password("volun123"), "VOLUNTARIO_TERRENO", True)
    ]
    
    for u in users:
        cursor.execute("SELECT email FROM usuarios WHERE email = %s", (u[4],))
        if cursor.fetchone():
            print(f"Usuario {u[4]} ya existe.")
        else:
            cursor.execute("""
                INSERT INTO usuarios (id, rut, nombre, apellido, email, password, rol, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, u)
            
    print("Seeding necesidades...")
    cursor.execute("SELECT count(*) FROM necesidades")
    count_nec = cursor.fetchone()[0]
    if count_nec == 0:
        cursor.execute("""
            INSERT INTO necesidades (nombre, categoria, cantidad_requerida, nivel_prioridad, ubicacion)
            VALUES 
            ('Bidones de Agua (5L)', 'Alimentos', 250, 'ALTA', 'VIÑA DEL MAR'),
            ('Kit de Construcción', 'Construcción', 45, 'MEDIA', 'QUILPUÉ'),
            ('Frazadas Térmicas', 'Higiene', 120, 'BAJA', 'VILLA ALEMANA')
        """)
        
    print("Seeding stock...")
    cursor.execute("SELECT count(*) FROM stock")
    count_stock = cursor.fetchone()[0]
    if count_stock == 0:
        cursor.execute("""
            INSERT INTO stock (nombre, categoria, cantidad_disponible, estado, ubicacion_bodega)
            VALUES 
            ('Arroz', 'Alimentos', 500, 'DISPONIBLE', 'Bodega Central'),
            ('Papel Higiénico', 'Higiene', 200, 'DISPONIBLE', 'Bodega 2')
        """)

    conn.commit()
    conn.close()
    print("Seeding finalizado.")

if __name__ == "__main__":
    seed_db()
