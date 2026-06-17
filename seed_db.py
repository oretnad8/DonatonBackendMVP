import mysql.connector
import random
from faker import Faker
import time

fake = Faker('es_CL') # Faker con localización chilena

# Datos realistas para el dominio logístico humanitario
COMUNAS = ["Valparaíso", "Viña del Mar", "Quilpué", "Villa Alemana", "Concón", "Limache", "Olmué", "Santiago", "Rancagua"]
TIPOS_ITEMS = ["Agua Embotellada", "Frazadas", "Kits de Aseo", "Alimentos No Perecibles", "Pañales", "Comida para Mascotas", "Mascarillas", "Herramientas de Remoción"]
URGENCIAS = ["ALTA", "MEDIA", "BAJA"]
ESTADOS_STOCK = ["DISPONIBLE", "DISPONIBLE", "DISPONIBLE", "RESERVADO", "AGOTADO"] # Mayor probabilidad de estar disponible

def connect_to_db():
    print("Conectando a la base de datos MySQL (donaton_db)...")
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="donaton_db"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar: {err}")
        print("Asegúrate de que MySQL esté corriendo y los microservicios de Spring Boot se hayan ejecutado al menos una vez para que creen las tablas.")
        return None

def seed_necesidades(cursor, num_records=20):
    print(f"Generando {num_records} registros de Necesidades...")
    query = """
        INSERT INTO necesidades (comuna, tipo_item, cantidad, urgencia) 
        VALUES (%s, %s, %s, %s)
    """
    for _ in range(num_records):
        comuna = random.choice(COMUNAS)
        tipo_item = random.choice(TIPOS_ITEMS)
        cantidad = random.randint(50, 1000)
        urgencia = random.choice(URGENCIAS)
        cursor.execute(query, (comuna, tipo_item, cantidad, urgencia))

def seed_stock(cursor, num_records=30):
    print(f"Generando {num_records} registros de Stock...")
    query = """
        INSERT INTO stock (comuna, tipo_item, cantidad_disponible, estado) 
        VALUES (%s, %s, %s, %s)
    """
    for _ in range(num_records):
        comuna = random.choice(COMUNAS)
        tipo_item = random.choice(TIPOS_ITEMS)
        cantidad = random.randint(100, 5000)
        estado = random.choice(ESTADOS_STOCK)
        cursor.execute(query, (comuna, tipo_item, cantidad, estado))

def main():
    conn = connect_to_db()
    if not conn:
        return

    cursor = conn.cursor()

    try:
        # Limpiar tablas para evitar acumular basura si se corre múltiples veces
        print("Limpiando tablas antiguas...")
        cursor.execute("TRUNCATE TABLE necesidades;")
        cursor.execute("TRUNCATE TABLE stock;")
        
        # Generar datos
        seed_necesidades(cursor, 50)
        seed_stock(cursor, 50)
        
        # Guardar cambios
        conn.commit()
        print("✅ Base de datos poblada exitosamente con datos realistas.")

    except mysql.connector.Error as err:
        print(f"Error al ejecutar consultas: {err}")
        print("Es posible que las tablas no existan aún. Ejecuta los microservicios Java primero para que Hibernate genere las tablas.")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
