import json
from kafka import KafkaConsumer
import psycopg2

# Configuración de PostgreSQL
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'kafka_demo',
    'user': 'kafka_user',
    'password': 'kafka_pass'
}

# Conexión a PostgreSQL
try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("Conectado a PostgreSQL ✅")
except Exception as e:
    print("❌ Error al conectar a la base de datos:", e)
    exit()

# Consumer de Kafka
consumer = KafkaConsumer(
    'user-registration',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='db-writer',
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("🔄 Esperando mensajes...")

# Escuchar y guardar en la base de datos
for message in consumer:
    user = message.value

    try:
        cursor.execute("""
            INSERT INTO user_registration (id, name, phone, email, latitude, longitude, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (
            user['id'],
            user['name'],
            user['phone'],
            user['email'],
            user['location']['lat'],
            user['location']['lon'],
            user['timestamp']
        ))
        conn.commit()
        print("✅ Insertado:", user['email'])

    except Exception as e:
        conn.rollback()
        print("❌ Error al insertar mensaje:", e)
