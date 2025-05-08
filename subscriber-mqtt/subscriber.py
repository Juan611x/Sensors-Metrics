import paho.mqtt.client as mqtt
import psycopg2
import json

# Configuración de conexión a PostgreSQL
DB_CONFIG = {
    'host': 'postgres',
    'database': 'saludiot',
    'user': 'postgres',
    'password': 'postgres'
}

# Función callback cuando llega un mensaje
def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic}")
    try:
        data = json.loads(msg.payload.decode())
        print("Datos recibidos:\n", json.dumps(data, indent=2))

        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO lectura_sensor (idSensor, unidad, valor, fecha_registro, nombre)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data.get("sensor_id"),
            data.get("unidad"),
            data.get("valor"),
            data.get("timestamp"),
            data.get("nombre")
        ))

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error al insertar en la base de datos: {e}")

# Configurar cliente MQTT
client = mqtt.Client()

client.connect("mosquitto", 1883)
client.subscribe("sensors/heartrate")
client.on_message = on_message

print("Subscriptor MQTT iniciado y escuchando en 'sensors/heartrate'")
client.loop_forever()
