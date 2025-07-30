import json
import time
from kafka import KafkaProducer
from faker import Faker


# Crea un generador de datos falsos
faker = Faker()

# Conecta con Kafka (usa localhost si estás usando Docker local)
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Envía 20 usuarios simulados
for _ in range(20):
    user = {
        "id": faker.uuid4(),
        "name": faker.name(),
        "phone": faker.phone_number(),
        "email": faker.email(),
        "location": {
            "lat": float(faker.latitude()),
            "lon": float(faker.longitude())
        },
        "timestamp": faker.iso8601()
    }

    # Envía al tópico "user-registration"
    producer.send('user-registration', value=user)
    print("Sent:", user)

    time.sleep(1)  # Espera 1 segundo entre envíos

producer.flush()
