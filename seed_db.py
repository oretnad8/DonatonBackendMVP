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
            # Verificar si la tabla usuarios ya fue creada por Hibernate
            cursor.execute("SHOW TABLES LIKE 'usuarios'")
            if cursor.fetchone():
                print("Tablas detectadas. Procediendo con el seeding...")
                break
            else:
                print(f"[{i+1}/{max_retries}] Base de datos conectada, pero la tabla 'usuarios' aun no existe. Esperando 5 segundos...")
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
            INSERT INTO necesidades (nombre, descripcion, cantidad_requerida, cantidad_actual, ubicacion, latitud, longitud, nivel_prioridad, estado, categoria, fecha_creacion, id_coordinador)
            VALUES 
            ('Bidones de Agua (5L)', 'Agua potable en bidones', 250, 50, 'VIÑA DEL MAR', -33.0245, -71.5518, 'ALTA', 'PENDIENTE', 'Alimentos', NOW(), NULL),
            ('Kit de Construcción', 'Kits básicos para reparación', 45, 10, 'QUILPUÉ', -33.0485, -71.4429, 'MEDIA', 'EN_PROCESO', 'Construcción', NOW(), NULL),
            ('Frazadas Térmicas', 'Frazadas para invierno', 120, 80, 'VILLA ALEMANA', -33.0422, -71.3733, 'BAJA', 'PENDIENTE', 'Higiene', NOW(), NULL)
        """)
        
    print("Seeding stock...")
    cursor.execute("SELECT count(*) FROM stock")
    count_stock = cursor.fetchone()[0]
    if count_stock == 0:
        cursor.execute("""
            INSERT INTO stock (sku, nombre, descripcion, cantidad_disponible, categoria, ubicacion_bodega, fecha_ingreso, fecha_vencimiento, estado)
            VALUES 
            ('ALI-001', 'Arroz', 'Arroz grado 2', 500, 'Alimentos', 'Bodega Central', NOW(), NULL, 'DISPONIBLE'),
            ('HIG-001', 'Papel Higiénico', 'Pack 4 rollos', 200, 'Higiene', 'Bodega 2', NOW(), NULL, 'DISPONIBLE')
        """)

    conn.commit()
    conn.close()
    print("Seeding finalizado.")

if __name__ == "__main__":
    seed_db()
